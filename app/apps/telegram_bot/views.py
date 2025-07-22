"""Telegram bot views – minimal version with only /start command."""

from __future__ import annotations

import logging
import re
import time
import os
from telebot import TeleBot, types
from django.conf import settings as django_settings
from apps.contacts import models as contacts_models
from apps.contacts.models import Testimonial

logger = logging.getLogger(__name__)

# Telegram bot initialisation
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = TeleBot(TELEGRAM_TOKEN)

# Chat/thread identifiers for testimonial moderation
REVIEWS_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))  # Group or channel where reviews are moderated
REVIEWS_THREAD_ID = os.getenv("TELEGRAM_REVIEWS_THREAD_ID")
REVIEWS_THREAD_ID = int(REVIEWS_THREAD_ID) if REVIEWS_THREAD_ID else None

# Thread id for contact form feedback
FEEDBACK_THREAD_ID = os.getenv("TELEGRAM_FEEDBACK_THREAD_ID")
FEEDBACK_THREAD_ID = int(FEEDBACK_THREAD_ID) if FEEDBACK_THREAD_ID else None

# Thread id for bookings within the same chat
BOOKING_THREAD_ID = os.getenv("TELEGRAM_BOOKING_THREAD_ID") or os.getenv("BOOKING_THREAD_ID")
BOOKING_THREAD_ID = int(BOOKING_THREAD_ID) if BOOKING_THREAD_ID else 43  # default 43


def normalize_phone_for_whatsapp(phone: str) -> str:
    """
    Нормализует номер телефона для WhatsApp ссылки.
    Поддерживает форматы СНГ стран: Россия (+7), Узбекистан (+998), Кыргызстан (+996).
    """
    if not phone:
        return ""
    
    # Убираем все нецифровые символы
    digits = re.sub(r"\D", "", phone)
    
    # Если номер пустой после очистки
    if not digits:
        return ""
    
    # Определяем код страны и нормализуем
    if digits.startswith('8') and len(digits) == 11:  # Россия: 8XXXXXXXXXX -> +7XXXXXXXXXX
        return '7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:  # Россия: 7XXXXXXXXXX -> +7XXXXXXXXXX
        return digits
    elif digits.startswith('996') and len(digits) == 12:  # Кыргызстан: 996XXXXXXXXX -> +996XXXXXXXXX
        return digits
    elif digits.startswith('998') and len(digits) == 12:  # Узбекистан: 998XXXXXXXXX -> +998XXXXXXXXX
        return digits
    elif digits.startswith('77') and len(digits) == 11:  # Казахстан: 77XXXXXXXXX -> +77XXXXXXXXX
        return digits
    elif len(digits) == 10:  # Локальный номер без кода страны
        # Пытаемся определить страну по первым цифрам
        if digits.startswith(('90', '91', '92', '93', '94', '95', '96', '97', '98', '99')):  # Россия
            return '7' + digits
        elif digits.startswith(('50', '55', '70', '77', '99')):  # Кыргызстан
            return '996' + digits
        elif digits.startswith(('88', '90', '91', '93', '94', '95', '97', '98', '99')):  # Узбекистан
            return '998' + digits
        else:  # По умолчанию Россия
            return '7' + digits
    elif len(digits) == 9:  # Кыргызстан без кода страны
        return '996' + digits
    
    # Если не удалось определить формат, возвращаем как есть
    return digits


def send_booking_message(booking: 'contacts_models.Booking') -> None:
    """Send booking details to dedicated booking topic."""
    chat_id = REVIEWS_CHAT_ID
    if not chat_id:
        logger.warning("No TELEGRAM_BOOKING_CHAT_ID / TELEGRAM_CHAT_ID configured – booking not sent")
        return

    text = (
        "🔔 <b>Новый заказ</b>\n\n"
        f"<b>🧹 Услуга:</b> {booking.service.title}\n"
        f"<b>👤 Клиент:</b> {booking.name}\n"
        f"<b>📞 Телефон:</b> <a href=\"tel:{booking.phone}\">{booking.phone}</a>\n"
        f"<b>🏠 Комнат:</b> {booking.rooms}\n"
        f"<b>🕒 Время:</b> {booking.created_at:%d.%m.%Y %H:%M}"
    )
    
    # Добавляем дополнительную информацию, если есть
    if booking.more:
        text += f"\n<b>📝 Дополнительно:</b> {booking.more}"

    # Нормализуем номер телефона для WhatsApp
    phone_digits = normalize_phone_for_whatsapp(booking.phone)

    keyboard = types.InlineKeyboardMarkup()
    if phone_digits:  # Только если номер валидный
        keyboard.add(
            types.InlineKeyboardButton("💬 WhatsApp", url=f"https://wa.me/{phone_digits}")
        )
    else:
        # Если номер невалидный, добавляем кнопку без ссылки
        keyboard.add(
            types.InlineKeyboardButton("📞 Номер некорректен", callback_data="invalid_phone")
        )

    bot.send_message(
        chat_id,
        text,
        parse_mode="HTML",
        message_thread_id=BOOKING_THREAD_ID,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


def send_contact_message(contact: 'contacts_models.ContactMessage') -> None:
    """Send new contact form message to Telegram chat."""
    if not REVIEWS_CHAT_ID:
        logger.warning("REVIEWS_CHAT_ID is not configured – contact message not sent")
        return

    text = (
        "<b>📬 Новое обращение</b>%0A%0A"
        f"<b>👤 Имя:</b> <i>{contact.name}</i>%0A"
        f"<b>📞 Телефон:</b> <code>{contact.phone}</code>%0A"
        f"<b>📌 Тема:</b> {contact.subject}%0A"
        "<b>💬 Сообщение:</b>%0A"
        f"{contact.message}"
    ).replace('%0A', '\n')
    bot.send_message(
        REVIEWS_CHAT_ID,
        text,
        parse_mode="HTML",
        message_thread_id=FEEDBACK_THREAD_ID,
    )


def send_testimonial_message(testimonial: Testimonial) -> None:
    """Send newly created testimonial to the Telegram moderation chat."""
    if not REVIEWS_CHAT_ID:
        logger.warning("REVIEWS_CHAT_ID is not configured – testimonial not sent")
        return

    text = (
        "📝 Новый отзыв\n\n"
        f"Имя: {testimonial.name}\n"
        f"Услуга: {testimonial.service}\n"
        f"Описание: {testimonial.description}"
    )

    keyboard = types.InlineKeyboardMarkup()
    approve_btn = types.InlineKeyboardButton(
        "✅ Вывести", callback_data=f"testimonial:{testimonial.id}:approve"
    )
    reject_btn = types.InlineKeyboardButton(
        "❌ Оставить", callback_data=f"testimonial:{testimonial.id}:reject"
    )
    keyboard.row(approve_btn, reject_btn)

    bot.send_message(
        REVIEWS_CHAT_ID,
        text,
        message_thread_id=REVIEWS_THREAD_ID,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("booking:"))
def booking_status_callback(call: types.CallbackQuery) -> None:
    """Handle status update buttons for bookings."""
    try:
        _prefix, booking_id, status_key = call.data.split(":")
    except ValueError:
        return

    status_map = {
        "accepted": "✅ Принято",
        "progress": "🚚 В работе",
        "done": "✔ Завершено",
    }
    status_label = status_map.get(status_key)
    if not status_label:
        return

    user = call.from_user
    manager = (user.first_name or "") + (f" {user.last_name}" if user.last_name else "")
    base_text = re.sub(r"\n\n(?:✅|🚚|✔).*$", "", call.message.text, flags=re.S)
    new_text = f"{base_text}\n\n{status_label} — <b>{manager.strip()}</b>"

    # Keep only WhatsApp button
    phone_digits = re.sub(r"\\D", "", base_text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("💬 WhatsApp", url=f"https://wa.me/{phone_digits}"))

    bot.edit_message_text(
        new_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )
    bot.answer_callback_query(call.id, status_label)


@bot.callback_query_handler(func=lambda call: call.data.startswith("testimonial:"))
def testimonial_callback(call: types.CallbackQuery) -> None:
    """Handle approve/reject actions for testimonials."""
    try:
        _, testimonial_id, action = call.data.split(":")
        testimonial = Testimonial.objects.filter(id=int(testimonial_id)).first()
        if not testimonial:
            bot.answer_callback_query(call.id, "Отзыв не найден!", show_alert=True)
            return

        if action == "approve":
            testimonial.show = True
            status = "✅ Принят"
        else:
            status = "❌ Отклонён"
        testimonial.save()

        new_text = (
            f"📝 Отзыв {testimonial.name}\n\n"
            f"Имя: {testimonial.name}\n"
            f"Услуга: {testimonial.service}\n"
            f"Описание: {testimonial.description}\n\n"
            f"Статус: {status}"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=new_text,
        )
        bot.answer_callback_query(call.id, status)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Error processing testimonial callback: %s", exc)
        bot.answer_callback_query(call.id, "Произошла ошибка", show_alert=True)


@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Handle the /start command – send greeting."""
    bot.send_message(
        message.chat.id,
        "👋 Привет! Это официальный бот проекта. Пишите /start, чтобы начать!",
    )


def run_polling() -> None:
    """Run the bot with basic restart logic."""
    while True:
        try:
            logger.info("Telegram bot polling started …")
            bot.polling(none_stop=True, interval=3)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Bot crashed with error: %s", exc)
            time.sleep(15)
            try:
                bot.stop_polling()
            except Exception as stop_exc:  # pylint: disable=broad-except
                logger.error("Error while stopping bot: %s", stop_exc)


if __name__ == "__main__":
    run_polling()