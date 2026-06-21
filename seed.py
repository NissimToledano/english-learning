"""Run this script once to add sample lessons to the database."""
from database import create_tables, SessionLocal, Lesson, Word, User
from auth import hash_password

create_tables()
db = SessionLocal()

# Ensure admin exists
if not db.query(User).filter(User.username == "admin").first():
    db.add(User(username="admin", email="admin@example.com", hashed_password=hash_password("admin123"), is_admin=True))
    db.commit()

# ── Sample Lesson 1: The Ocean ────────────────────────────────────────────────
if not db.query(Lesson).filter(Lesson.title == "Life Under the Sea").first():
    lesson1 = Lesson(
        title="Life Under the Sea",
        topic="Nature & Animals",
        level="intermediate",
        week_number=1,
        is_published=True,
        reading_text="""The ocean covers more than 70 percent of Earth's surface and is home to an incredible variety of life. From tiny plankton to enormous whales, marine creatures have adapted to survive in one of the most challenging environments on our planet.

Coral reefs are among the most diverse ecosystems in the ocean. These underwater structures are built by tiny animals called coral polyps. Although coral reefs cover less than one percent of the ocean floor, they provide habitat for about 25 percent of all marine species.

Deep in the ocean, where sunlight cannot reach, mysterious creatures glow in the darkness using a process called bioluminescence. These animals produce their own light to attract prey, communicate with others, or confuse predators.

Unfortunately, human activities are threatening ocean life. Pollution, overfishing, and climate change are causing significant damage to marine ecosystems. Scientists and conservationists are working hard to protect these vital environments for future generations."""
    )
    db.add(lesson1)
    db.flush()

    words1 = [
        Word(lesson_id=lesson1.id, english="surface", hebrew="פני שטח", phonetic="/ˈsɜːfɪs/", word_type="noun", example_sentence="The ball floated on the surface of the water."),
        Word(lesson_id=lesson1.id, english="marine", hebrew="ימי", phonetic="/məˈriːn/", word_type="adjective", example_sentence="Marine biologists study life in the ocean."),
        Word(lesson_id=lesson1.id, english="creature", hebrew="יצור", phonetic="/ˈkriːtʃər/", word_type="noun", example_sentence="The strange creature moved slowly along the ocean floor."),
        Word(lesson_id=lesson1.id, english="adapted", hebrew="הסתגל", phonetic="/əˈdæptɪd/", word_type="verb", example_sentence="Animals have adapted to survive in cold climates."),
        Word(lesson_id=lesson1.id, english="ecosystem", hebrew="מערכת אקולוגית", phonetic="/ˈiːkəʊˌsɪstəm/", word_type="noun", example_sentence="The forest ecosystem depends on clean water."),
        Word(lesson_id=lesson1.id, english="diverse", hebrew="מגוון", phonetic="/daɪˈvɜːs/", word_type="adjective", example_sentence="Our school has a diverse group of students."),
        Word(lesson_id=lesson1.id, english="habitat", hebrew="בית גידול", phonetic="/ˈhæbɪtæt/", word_type="noun", example_sentence="The panda's habitat is being destroyed by deforestation."),
        Word(lesson_id=lesson1.id, english="species", hebrew="מין", phonetic="/ˈspiːʃiːz/", word_type="noun", example_sentence="There are over 8 million species on Earth."),
        Word(lesson_id=lesson1.id, english="bioluminescence", hebrew="ביולומינסנציה", phonetic="/ˌbaɪəʊˌluːmɪˈnesns/", word_type="noun", example_sentence="Bioluminescence makes some deep-sea fish glow."),
        Word(lesson_id=lesson1.id, english="predator", hebrew="טורף", phonetic="/ˈpredətər/", word_type="noun", example_sentence="The lion is a predator that hunts other animals."),
        Word(lesson_id=lesson1.id, english="pollution", hebrew="זיהום", phonetic="/pəˈluːʃən/", word_type="noun", example_sentence="Pollution in rivers harms fish and other wildlife."),
        Word(lesson_id=lesson1.id, english="conservation", hebrew="שמירת טבע", phonetic="/ˌkɒnsəˈveɪʃən/", word_type="noun", example_sentence="Conservation efforts have helped protect endangered animals."),
        Word(lesson_id=lesson1.id, english="significant", hebrew="משמעותי", phonetic="/sɪɡˈnɪfɪkənt/", word_type="adjective", example_sentence="There was a significant improvement in his grades."),
        Word(lesson_id=lesson1.id, english="vital", hebrew="חיוני", phonetic="/ˈvaɪtəl/", word_type="adjective", example_sentence="It is vital to drink enough water every day."),
        Word(lesson_id=lesson1.id, english="generation", hebrew="דור", phonetic="/ˌdʒenəˈreɪʃən/", word_type="noun", example_sentence="Each generation learns from the one before it."),
    ]
    for w in words1:
        db.add(w)

# ── Sample Lesson 2: Social Media ─────────────────────────────────────────────
if not db.query(Lesson).filter(Lesson.title == "Social Media and Teens").first():
    lesson2 = Lesson(
        title="Social Media and Teens",
        topic="Technology & Society",
        level="intermediate",
        week_number=2,
        is_published=True,
        reading_text="""Social media platforms have become a major part of daily life for teenagers around the world. Apps like Instagram, TikTok, and YouTube allow young people to share content, connect with friends, and discover new interests.

However, spending too much time on social media can have negative consequences. Research shows that excessive screen time may affect sleep quality, reduce focus, and contribute to feelings of anxiety or low self-esteem when teenagers constantly compare themselves to others.

On the positive side, social media can be a powerful tool for learning and creativity. Many young people use these platforms to showcase their talents in art, music, or coding. Online communities also provide support for teens who feel isolated or misunderstood in their everyday lives.

Experts recommend that teenagers maintain a healthy balance. Setting limits on daily usage, taking regular breaks, and being mindful of the content they consume can help young people enjoy the benefits of social media while avoiding its pitfalls."""
    )
    db.add(lesson2)
    db.flush()

    words2 = [
        Word(lesson_id=lesson2.id, english="platform", hebrew="פלטפורמה", phonetic="/ˈplætfɔːm/", word_type="noun", example_sentence="YouTube is a popular video-sharing platform."),
        Word(lesson_id=lesson2.id, english="consequences", hebrew="תוצאות/השלכות", phonetic="/ˈkɒnsɪkwənsɪz/", word_type="noun", example_sentence="He faced serious consequences for cheating on the test."),
        Word(lesson_id=lesson2.id, english="excessive", hebrew="מוגזם", phonetic="/ɪkˈsesɪv/", word_type="adjective", example_sentence="Excessive sugar can be bad for your health."),
        Word(lesson_id=lesson2.id, english="anxiety", hebrew="חרדה", phonetic="/æŋˈzaɪəti/", word_type="noun", example_sentence="She felt anxiety before her big presentation."),
        Word(lesson_id=lesson2.id, english="self-esteem", hebrew="דימוי עצמי", phonetic="/ˌself ɪˈstiːm/", word_type="noun", example_sentence="Success in sports boosted his self-esteem."),
        Word(lesson_id=lesson2.id, english="compare", hebrew="להשוות", phonetic="/kəmˈpeər/", word_type="verb", example_sentence="Don't compare yourself to others – be yourself."),
        Word(lesson_id=lesson2.id, english="creativity", hebrew="יצירתיות", phonetic="/ˌkriːeɪˈtɪvɪti/", word_type="noun", example_sentence="Painting helps express creativity."),
        Word(lesson_id=lesson2.id, english="showcase", hebrew="להציג/לשווין", phonetic="/ˈʃəʊkeɪs/", word_type="verb", example_sentence="The fair gave students a chance to showcase their projects."),
        Word(lesson_id=lesson2.id, english="isolated", hebrew="מבודד", phonetic="/ˈaɪsəleɪtɪd/", word_type="adjective", example_sentence="Moving to a new city made her feel isolated."),
        Word(lesson_id=lesson2.id, english="recommend", hebrew="להמליץ", phonetic="/ˌrekəˈmend/", word_type="verb", example_sentence="I would recommend this book to any science lover."),
        Word(lesson_id=lesson2.id, english="balance", hebrew="איזון", phonetic="/ˈbæləns/", word_type="noun", example_sentence="A healthy balance between work and rest is important."),
        Word(lesson_id=lesson2.id, english="mindful", hebrew="מודע/קשוב", phonetic="/ˈmaɪndfəl/", word_type="adjective", example_sentence="Be mindful of the words you use when speaking to others."),
        Word(lesson_id=lesson2.id, english="consume", hebrew="לצרוך", phonetic="/kənˈsjuːm/", word_type="verb", example_sentence="People consume more energy in winter."),
        Word(lesson_id=lesson2.id, english="pitfall", hebrew="מלכודת/מכשול", phonetic="/ˈpɪtfɔːl/", word_type="noun", example_sentence="One common pitfall is spending too much money on ads."),
    ]
    for w in words2:
        db.add(w)

db.commit()
print("✅ Sample lessons created successfully!")
print("Admin login: username=admin, password=admin123")
db.close()
