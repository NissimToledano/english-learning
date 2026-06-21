"""
Run this script to seed all 20 lessons + users (Hallel, Yair, admin).
Safe to re-run - skips existing records.
"""
from database import create_tables, SessionLocal, Lesson, Word, User
from auth import hash_password

USERS = [
    {"username": "admin",  "email": "admin@english.com",  "password": "admin123",  "is_admin": True,  "level": "advanced"},
    {"username": "hallel", "email": "hallel@english.com", "password": "hallel123", "is_admin": False, "level": "intermediate"},
    {"username": "yair",   "email": "yair@english.com",   "password": "yair123",   "is_admin": False, "level": "beginner"},
]

LESSONS = [

# ═══════════════════════ BEGINNER (weeks 1-7) ═══════════════════════

{
"title": "Animals at the Zoo",
"topic": "Nature & Animals",
"level": "beginner",
"week": 1,
"text": """Visiting a zoo is a wonderful experience for people of all ages. At the zoo, you can see hundreds of different animals from all over the world. Large mammals like elephants and giraffes live in wide open spaces that look like their natural habitats. In the reptile house, you can observe snakes, lizards, and turtles up close.

The zoo also cares for endangered species — animals that are in danger of disappearing from the wild forever. Zookeepers feed the animals every day and make sure they stay healthy. Many zoos run special education programs to teach visitors about wildlife and conservation.

When you leave the zoo, you will probably feel a new respect for the amazing creatures that share our planet with us.""",
"words": [
    ("mammal","יונק","/ˈmæməl/","noun","A whale is a mammal that lives in the ocean."),
    ("reptile","זוחל","/ˈreptaɪl/","noun","A crocodile is a large reptile found in tropical rivers."),
    ("endangered","בסכנת הכחדה","/ɪnˈdeɪndʒərd/","adjective","The tiger is an endangered animal that needs protection."),
    ("habitat","בית גידול","/ˈhæbɪtæt/","noun","The panda's natural habitat is the bamboo forest."),
    ("carnivore","טורף","/ˈkɑːrnɪvɔːr/","noun","A lion is a carnivore that eats meat."),
    ("herbivore","אוכל צמחים","/ˈhɜːrbɪvɔːr/","noun","A cow is a herbivore that eats only plants."),
    ("observe","לצפות","/əbˈzɜːrv/","verb","We observed the lions sleeping in the sun."),
    ("exhibit","תצוגה","/ɪɡˈzɪbɪt/","noun","The new exhibit at the zoo shows Arctic animals."),
    ("wild","טבע/בר","/waɪld/","adjective","Wolves live in the wild and hunt their own food."),
    ("conservation","שמירת טבע","/ˌkɒnsəˈveɪʃən/","noun","Conservation programs help protect rare animals."),
]},

{
"title": "My School Day",
"topic": "Education",
"level": "beginner",
"week": 2,
"text": """Every morning, I wake up early and get ready for school. I pack my school bag with all my textbooks, notebooks, and pencils. The school day starts at eight o'clock with mathematics, which is my favorite subject.

After morning lessons, I go to the cafeteria for lunch with my friends. We talk about our assignments and what we plan to do in the afternoon. After lunch, we have physical education, where we play basketball in the gymnasium.

At the end of the day, our teacher reminds us about our homework. I come home, have a snack, and then sit down to study. I try to finish all my assignments before dinner so I can relax in the evening. Being organized helps me do well at school.""",
"words": [
    ("textbook","ספר לימוד","/ˈtekstbʊk/","noun","Please open your textbook to page fifteen."),
    ("subject","מקצוע","/ˈsʌbdʒɪkt/","noun","My favorite subject at school is science."),
    ("assignment","מטלה","/əˈsaɪnmənt/","noun","Did you finish the assignment for tomorrow?"),
    ("cafeteria","קפיטריה","/ˌkæfɪˈtɪəriə/","noun","We eat lunch together in the school cafeteria."),
    ("gymnasium","אולם ספורט","/dʒɪmˈneɪziəm/","noun","We play basketball in the school gymnasium."),
    ("concentrate","להתרכז","/ˈkɒnsəntreɪt/","verb","It is hard to concentrate when there is loud noise."),
    ("organized","מאורגן","/ˈɔːrɡənaɪzd/","adjective","Being organized helps you save time every day."),
    ("schedule","לוח זמנים","/ˈʃedjuːl/","noun","The teacher gave us the schedule for next week."),
    ("principal","מנהל/ת בית ספר","/ˈprɪnsɪpəl/","noun","The principal gave a speech at the school assembly."),
    ("remind","להזכיר","/rɪˈmaɪnd/","verb","Please remind me to call my friend after school."),
]},

{
"title": "Food Around the World",
"topic": "Food & Culture",
"level": "beginner",
"week": 3,
"text": """Food is an important part of every culture around the world. Each country has its own traditional dishes that reflect the history and environment of its people. In Italy, pizza and pasta are national favorites. In Japan, sushi and ramen are popular meals. In Israel, falafel and hummus are loved by almost everyone.

When people travel, they often try new and exciting foods. Street food markets are great places to taste local recipes made with fresh ingredients. Some dishes are spicy, while others are sweet or salty.

Learning to cook a new recipe is a wonderful way to learn about another culture. Food can bring people together and create happy memories around the dinner table.""",
"words": [
    ("cuisine","מטבח של מדינה","/kwɪˈziːn/","noun","Italian cuisine is famous for its pasta and pizza."),
    ("ingredient","מרכיב","/ɪnˈɡriːdiənt/","noun","Flour, eggs, and sugar are the main ingredients in cake."),
    ("recipe","מתכון","/ˈresɪpi/","noun","My grandmother taught me her secret recipe for soup."),
    ("flavor","טעם","/ˈfleɪvər/","noun","This ice cream has a wonderful vanilla flavor."),
    ("spicy","חריף","/ˈspaɪsi/","adjective","The curry was very spicy and made my mouth burn."),
    ("tradition","מסורת","/trəˈdɪʃən/","noun","It is a tradition in our family to eat together on Friday."),
    ("delicious","טעים מאוד","/dɪˈlɪʃəs/","adjective","The chocolate cake was absolutely delicious."),
    ("appetite","תיאבון","/ˈæpɪtaɪt/","noun","Exercise always gives me a big appetite."),
    ("market","שוק","/ˈmɑːrkɪt/","noun","We bought fresh vegetables at the local market."),
    ("culture","תרבות","/ˈkʌltʃər/","noun","Learning about culture helps us understand other people."),
]},

{
"title": "Sports and Being Active",
"topic": "Sports & Health",
"level": "beginner",
"week": 4,
"text": """Playing sports is one of the best ways to stay healthy and make new friends. There are many different types of sports — some are played in teams, like football and basketball, while others are individual, like swimming or tennis.

When you join a sports team, you learn important skills like teamwork, discipline, and how to deal with winning and losing. A good coach helps players improve their skills and work together as a team. Regular physical activity also strengthens your body and improves your mood.

Many famous athletes started playing their sport as young children. With enough practice and dedication, anyone can improve. It does not matter if you are the best player — what matters is that you enjoy the game and give your best effort.""",
"words": [
    ("athlete","ספורטאי","/ˈæθliːt/","noun","The athlete trained every morning before school."),
    ("teamwork","עבודת צוות","/ˈtiːmwɜːrk/","noun","Good teamwork helps a team win games."),
    ("coach","מאמן","/koʊtʃ/","noun","The coach taught us how to improve our running technique."),
    ("compete","להתחרות","/kəmˈpiːt/","verb","She loves to compete in swimming competitions."),
    ("championship","אליפות","/ˈtʃæmpiənʃɪp/","noun","Our team won the national championship last year."),
    ("discipline","משמעת","/ˈdɪsɪplɪn/","noun","Discipline is the key to becoming a great athlete."),
    ("victory","ניצחון","/ˈvɪktəri/","noun","The team celebrated their victory with a big party."),
    ("effort","מאמץ","/ˈefərt/","noun","She put a lot of effort into her training."),
    ("physical","פיזי/גופני","/ˈfɪzɪkəl/","adjective","Regular physical activity keeps your body strong."),
    ("improve","להשתפר","/ɪmˈpruːv/","verb","Practice every day and you will improve quickly."),
]},

{
"title": "Weather and Seasons",
"topic": "Nature",
"level": "beginner",
"week": 5,
"text": """The weather changes throughout the year depending on the season. In spring, flowers begin to bloom and the days become longer and warmer. Summer is the hottest season, with long sunny days and high temperatures. Many people go to the beach or travel during summer vacation.

In autumn, the leaves on trees change color from green to yellow, orange, and red before falling to the ground. The air becomes cooler and people start wearing warmer clothes. Winter is the coldest season, and in some places it snows.

The weather affects what we wear, what we eat, and what activities we do. Some people love hot weather, while others prefer cold winters. Checking the weather forecast before going outside is always a good idea.""",
"words": [
    ("temperature","טמפרטורה","/ˈtemprɪtʃər/","noun","The temperature outside is very high today."),
    ("forecast","תחזית מזג אוויר","/ˈfɔːrkæst/","noun","The weather forecast says it will rain tomorrow."),
    ("bloom","לפרוח","/bluːm/","verb","The flowers begin to bloom in spring."),
    ("season","עונה","/ˈsiːzən/","noun","My favorite season is autumn because of the colors."),
    ("temperature","טמפרטורה","/ˈtemprɪtʃər/","noun","The temperature dropped below zero last night."),
    ("humid","לח","/ˈhjuːmɪd/","adjective","The summer air is hot and humid near the sea."),
    ("drought","בצורת","/draʊt/","noun","The drought lasted for three months with no rain."),
    ("freezing","קופא/קר מאוד","/ˈfriːzɪŋ/","adjective","It was freezing outside, so we stayed indoors."),
    ("atmosphere","אטמוספרה","/ˈætməsfɪər/","noun","The atmosphere protects Earth from the sun's radiation."),
    ("climate","אקלים","/ˈklaɪmɪt/","noun","Israel has a warm and dry climate in summer."),
]},

{
"title": "My Hobbies",
"topic": "Lifestyle",
"level": "beginner",
"week": 6,
"text": """A hobby is an activity that you enjoy doing in your free time. Hobbies are important because they help you relax, learn new skills, and meet people who share the same interests.

Some popular hobbies among teenagers include drawing, playing musical instruments, reading, gaming, and cooking. Physical hobbies like cycling, dancing, or hiking are great for your health. Creative hobbies like painting or writing help you express your feelings and imagination.

Having a hobby can also be useful for your future. Many people have turned their hobby into a successful career. For example, a teenager who loves photography might become a professional photographer one day. Whatever hobby you choose, the most important thing is to enjoy it and keep practicing.""",
"words": [
    ("hobby","תחביב","/ˈhɒbi/","noun","My favorite hobby is playing the guitar."),
    ("creative","יצירתי","/kriˈeɪtɪv/","adjective","She is very creative and loves painting."),
    ("inspire","לעורר השראה","/ɪnˈspaɪər/","verb","Great music can inspire people to express themselves."),
    ("passion","תשוקה","/ˈpæʃən/","noun","He has a passion for photography and takes pictures every day."),
    ("talent","כישרון","/ˈtælənt/","noun","She has a natural talent for playing the piano."),
    ("skill","מיומנות","/skɪl/","noun","Drawing is a skill that you can learn with practice."),
    ("express","לבטא","/ɪkˈspres/","verb","Art is a wonderful way to express your feelings."),
    ("career","קריירה","/kəˈrɪər/","noun","She decided to make photography her career."),
    ("imagination","דמיון","/ɪˌmædʒɪˈneɪʃən/","noun","Children have a very rich imagination."),
    ("relaxing","מרגיע","/rɪˈlæksɪŋ/","adjective","Reading a good book is very relaxing."),
]},

{
"title": "Shopping and Money",
"topic": "Daily Life",
"level": "beginner",
"week": 7,
"text": """Shopping is something most people do regularly. We shop for food at the supermarket, for clothes at stores, and for electronics online. Before going shopping, it is a good idea to make a list so you do not forget anything or spend too much money.

When you go shopping, you might see sales and discounts that make products cheaper. A smart shopper compares prices and looks for the best quality at the lowest price. It is also important to keep your receipt in case you need to return something.

Learning to manage your money wisely is an important life skill. Creating a budget — a plan for how to spend your money — helps you save for things that really matter to you, like a new phone, a trip, or a gift for a friend.""",
"words": [
    ("discount","הנחה","/ˈdɪskaʊnt/","noun","The shop is offering a fifty percent discount today."),
    ("receipt","קבלה","/rɪˈsiːt/","noun","Keep your receipt in case you want to return the item."),
    ("budget","תקציב","/ˈbʌdʒɪt/","noun","I have a budget of fifty shekels for lunch."),
    ("purchase","לרכוש/רכישה","/ˈpɜːrtʃəs/","verb","I purchased a new bag at the market."),
    ("quality","איכות","/ˈkwɒlɪti/","noun","This brand is known for its high quality."),
    ("compare","להשוות","/kəmˈpeər/","verb","Always compare prices before you buy something expensive."),
    ("refund","החזר כסף","/ˈriːfʌnd/","noun","I got a full refund because the product was broken."),
    ("afford","להרשות לעצמי","/əˈfɔːrd/","verb","I cannot afford to buy a new laptop right now."),
    ("bargain","מציאה","/ˈbɑːrɡɪn/","noun","This jacket was a real bargain — only twenty dollars!"),
    ("save","לחסוך","/seɪv/","verb","I try to save some money every week."),
]},

# ═══════════════════════ INTERMEDIATE (weeks 8-16) ═══════════════════════

{
"title": "Life Under the Sea",
"topic": "Nature & Animals",
"level": "intermediate",
"week": 8,
"text": """The ocean covers more than 70 percent of Earth's surface and is home to an incredible variety of life. From tiny plankton to enormous whales, marine creatures have adapted to survive in one of the most challenging environments on our planet.

Coral reefs are among the most diverse ecosystems in the ocean. These underwater structures are built by tiny animals called coral polyps. Although coral reefs cover less than one percent of the ocean floor, they provide habitat for about 25 percent of all marine species.

Deep in the ocean, where sunlight cannot reach, mysterious creatures glow in the darkness using a process called bioluminescence. These animals produce their own light to attract prey, communicate with others, or confuse predators.

Unfortunately, human activities are threatening ocean life. Pollution, overfishing, and climate change are causing significant damage to marine ecosystems.""",
"words": [
    ("marine","ימי","/məˈriːn/","adjective","Marine biologists study life in the ocean."),
    ("creature","יצור","/ˈkriːtʃər/","noun","The strange creature moved slowly along the ocean floor."),
    ("ecosystem","מערכת אקולוגית","/ˈiːkəʊˌsɪstəm/","noun","The forest ecosystem depends on clean water."),
    ("diverse","מגוון","/daɪˈvɜːs/","adjective","Our school has a diverse group of students from many countries."),
    ("habitat","בית גידול","/ˈhæbɪtæt/","noun","The panda's habitat is being destroyed by deforestation."),
    ("species","מין","/ˈspiːʃiːz/","noun","There are over 8 million species on Earth."),
    ("bioluminescence","ביולומינסנציה","/ˌbaɪəʊˌluːmɪˈnesns/","noun","Bioluminescence makes some deep-sea fish glow in the dark."),
    ("predator","טורף","/ˈpredətər/","noun","The lion is a predator that hunts other animals."),
    ("pollution","זיהום","/pəˈluːʃən/","noun","Pollution in rivers harms fish and other wildlife."),
    ("significant","משמעותי","/sɪɡˈnɪfɪkənt/","adjective","There was a significant improvement in her test scores."),
    ("adapted","הסתגל","/əˈdæptɪd/","verb","Animals have adapted to survive in cold climates."),
    ("threaten","לאיים","/ˈθretən/","verb","Human activities threaten many species with extinction."),
]},

{
"title": "Social Media and Teens",
"topic": "Technology & Society",
"level": "intermediate",
"week": 9,
"text": """Social media platforms have become a major part of daily life for teenagers around the world. Apps like Instagram, TikTok, and YouTube allow young people to share content, connect with friends, and discover new interests.

However, spending too much time on social media can have negative consequences. Research shows that excessive screen time may affect sleep quality, reduce focus, and contribute to feelings of anxiety or low self-esteem when teenagers constantly compare themselves to others.

On the positive side, social media can be a powerful tool for learning and creativity. Many young people use these platforms to showcase their talents in art, music, or coding. Online communities also provide support for teens who feel isolated.

Experts recommend that teenagers maintain a healthy balance and set daily limits on their usage.""",
"words": [
    ("platform","פלטפורמה","/ˈplætfɔːm/","noun","YouTube is a popular video-sharing platform."),
    ("consequences","השלכות","/ˈkɒnsɪkwənsɪz/","noun","He faced serious consequences for cheating on the test."),
    ("excessive","מוגזם","/ɪkˈsesɪv/","adjective","Excessive sugar can be bad for your health."),
    ("anxiety","חרדה","/æŋˈzaɪəti/","noun","She felt anxiety before her big presentation."),
    ("self-esteem","דימוי עצמי","/ˌself ɪˈstiːm/","noun","Success in sports boosted his self-esteem."),
    ("compare","להשוות","/kəmˈpeər/","verb","Don't compare yourself to others — be yourself."),
    ("creativity","יצירתיות","/ˌkriːeɪˈtɪvɪti/","noun","Painting is a great way to express creativity."),
    ("showcase","להציג","/ˈʃəʊkeɪs/","verb","The fair gave students a chance to showcase their work."),
    ("isolated","מבודד","/ˈaɪsəleɪtɪd/","adjective","Moving to a new city made her feel isolated."),
    ("recommend","להמליץ","/ˌrekəˈmend/","verb","I would recommend this book to any science lover."),
    ("balance","איזון","/ˈbæləns/","noun","A healthy balance between work and rest is important."),
    ("mindful","מודע/קשוב","/ˈmaɪndfəl/","adjective","Be mindful of the words you use when speaking to others."),
]},

{
"title": "Space Exploration",
"topic": "Science & Technology",
"level": "intermediate",
"week": 10,
"text": """Humans have always looked up at the night sky and wondered what lies beyond our planet. Space exploration began in the 1950s, when the Soviet Union launched Sputnik, the first artificial satellite. In 1969, American astronaut Neil Armstrong became the first human to walk on the Moon.

Today, space agencies like NASA and private companies like SpaceX are working to send humans to Mars. Scientists are also searching for signs of life on other planets and studying distant galaxies with powerful telescopes like the James Webb Space Telescope.

Living in space is extremely challenging. Astronauts must deal with weightlessness, radiation, and the psychological effects of being far from Earth for long periods. Despite these challenges, space exploration continues to inspire millions of people and pushes the boundaries of human knowledge.""",
"words": [
    ("satellite","לוויין","/ˈsætəlaɪt/","noun","The satellite orbits the Earth every ninety minutes."),
    ("astronaut","אסטרונאוט","/ˈæstrənɔːt/","noun","The astronaut spent six months on the space station."),
    ("galaxy","גלקסיה","/ˈɡæləksi/","noun","Our solar system is inside the Milky Way galaxy."),
    ("weightlessness","חוסר משקל","/ˈweɪtləsnəs/","noun","Astronauts experience weightlessness in space."),
    ("radiation","קרינה","/ˌreɪdiˈeɪʃən/","noun","The sun produces harmful radiation that can damage skin."),
    ("telescope","טלסקופ","/ˈtelɪskəʊp/","noun","With a telescope, you can see craters on the moon."),
    ("exploration","חקר/סיור","/ˌekspləˈreɪʃən/","noun","The exploration of Mars is a major scientific goal."),
    ("launch","לשגר","/lɔːntʃ/","verb","NASA plans to launch a new rocket next year."),
    ("boundaries","גבולות","/ˈbaʊndəriz/","noun","Science always pushes the boundaries of what we know."),
    ("inspire","לעורר השראה","/ɪnˈspaɪər/","verb","The moon landing inspired a whole generation of scientists."),
    ("psychological","פסיכולוגי","/ˌsaɪkəˈlɒdʒɪkəl/","adjective","Being isolated has a psychological effect on people."),
    ("distant","רחוק","/ˈdɪstənt/","adjective","Scientists study distant stars using powerful telescopes."),
]},

{
"title": "Climate Change",
"topic": "Environment",
"level": "intermediate",
"week": 11,
"text": """Climate change is one of the biggest challenges facing our planet today. The Earth's average temperature has been rising steadily over the past century, mainly because of human activities such as burning fossil fuels and cutting down forests.

This rise in temperature is causing serious problems around the world. Glaciers and polar ice caps are melting, causing sea levels to rise. Extreme weather events like hurricanes, droughts, and heatwaves are becoming more frequent and more powerful. Many plant and animal species are struggling to survive as their natural habitats change.

Scientists agree that we must reduce our carbon emissions urgently to slow down global warming. Governments, companies, and individuals all have a role to play. Switching to renewable energy, reducing waste, and planting trees are all steps that can make a real difference.""",
"words": [
    ("fossil fuels","דלקים מאובנים","/ˈfɒsəl fjuːəlz/","noun","Burning fossil fuels releases carbon dioxide into the air."),
    ("glacier","קרחון","/ˈɡleɪsiər/","noun","The glacier has been melting rapidly due to global warming."),
    ("emission","פליטה","/ɪˈmɪʃən/","noun","Cars produce harmful emissions that pollute the air."),
    ("renewable","מתחדש","/rɪˈnjuːəbəl/","adjective","Solar power is a renewable source of energy."),
    ("drought","בצורת","/draʊt/","noun","The drought caused crops to fail across the region."),
    ("heatwave","גל חום","/ˈhiːtweɪv/","noun","The heatwave last summer broke temperature records."),
    ("urgent","דחוף","/ˈɜːrdʒənt/","adjective","It is urgent that we reduce pollution immediately."),
    ("reduce","להפחית","/rɪˈdjuːs/","verb","We must reduce the amount of plastic we use every day."),
    ("habitat","בית גידול","/ˈhæbɪtæt/","noun","Deforestation destroys the habitat of many animals."),
    ("global warming","התחממות גלובלית","/ˈɡloʊbəl ˈwɔːrmɪŋ/","noun","Global warming is causing ice to melt at the poles."),
    ("frequent","תכוף","/ˈfriːkwənt/","adjective","Extreme storms are becoming more frequent each year."),
    ("individual","פרט/יחיד","/ˌɪndɪˈvɪdʒuəl/","noun","Every individual can make a difference by reducing waste."),
]},

{
"title": "Music Around the World",
"topic": "Arts & Culture",
"level": "intermediate",
"week": 12,
"text": """Music is a universal language that connects people across cultures and generations. Every country has its own musical traditions, instruments, and styles that reflect the history and emotions of its people.

In West Africa, drums play a central role in storytelling and celebration. In India, classical music is based on complex patterns called ragas, which are designed to express specific emotions. In the United States, jazz and blues music grew out of the African-American experience and later influenced rock, pop, and hip-hop around the world.

Today, musicians from different countries collaborate and mix styles to create exciting new sounds. Streaming platforms have made it possible to listen to music from any corner of the world in seconds. Music has the power to heal, unite, and inspire — it is one of the most important forms of human expression.""",
"words": [
    ("universal","אוניברסלי","/ˌjuːnɪˈvɜːrsəl/","adjective","Laughter is a universal form of communication."),
    ("tradition","מסורת","/trəˈdɪʃən/","noun","Playing the violin is a tradition in his family."),
    ("instrument","כלי נגינה","/ˈɪnstrəmənt/","noun","She plays three different instruments: guitar, piano, and flute."),
    ("collaborate","לשתף פעולה","/kəˈlæbəreɪt/","verb","The two artists collaborated to write a new song."),
    ("influence","להשפיע","/ˈɪnfluəns/","verb","Jazz music has influenced many modern music styles."),
    ("expression","ביטוי","/ɪkˈspreʃən/","noun","Music is a powerful form of emotional expression."),
    ("rhythm","קצב","/ˈrɪðəm/","noun","She clapped her hands in rhythm with the music."),
    ("emotion","רגש","/ɪˈmoʊʃən/","noun","The song was full of deep emotion and made everyone cry."),
    ("streaming","סטרימינג","/ˈstriːmɪŋ/","noun","Streaming services have changed the way we listen to music."),
    ("generation","דור","/ˌdʒenəˈreɪʃən/","noun","This song has been loved by every generation."),
    ("heal","לרפא","/hiːl/","verb","Music has the power to heal emotional pain."),
    ("complex","מורכב","/ˈkɒmpleks/","adjective","The rhythm pattern is very complex and hard to learn."),
]},

{
"title": "The Olympic Games",
"topic": "Sports",
"level": "intermediate",
"week": 13,
"text": """The Olympic Games are the world's greatest sporting event, bringing together athletes from more than 200 countries to compete for gold, silver, and bronze medals. The modern Olympics began in Athens, Greece, in 1896, inspired by the ancient Greek Olympic Games that were held over 2,500 years ago.

The Summer Olympics feature over 30 sports, including athletics, swimming, gymnastics, and football. The Winter Olympics include sports like skiing, ice skating, and snowboarding. Every four years, the host city spends years preparing stadiums, accommodation, and transportation for thousands of athletes and millions of spectators.

The Olympic motto — "Faster, Higher, Stronger" — captures the spirit of competition and the human desire to push beyond limits. Beyond medals, the Olympics promote peace and unity among nations, reminding us that sport has the power to bring the world together.""",
"words": [
    ("athlete","ספורטאי","/ˈæθliːt/","noun","The athlete won three gold medals at the Olympics."),
    ("medal","מדליה","/ˈmedəl/","noun","She trained for years to win an Olympic medal."),
    ("compete","להתחרות","/kəmˈpiːt/","verb","Over 10,000 athletes competed in the last Olympics."),
    ("spectator","צופה","/spekˈteɪtər/","noun","Thousands of spectators cheered for their team."),
    ("stadium","אצטדיון","/ˈsteɪdiəm/","noun","The stadium was full of excited fans."),
    ("motto","מוטו/סיסמה","/ˈmɒtoʊ/","noun","The school's motto is 'Learn, Grow, Succeed'."),
    ("host","לארח","/hoʊst/","verb","Paris will host the next Olympic Games."),
    ("unity","אחדות","/ˈjuːnɪti/","noun","The event was a symbol of unity among nations."),
    ("promote","לקדם","/prəˈmoʊt/","verb","The Olympics promote peace and international friendship."),
    ("ancient","עתיק","/ˈeɪnʃənt/","adjective","The ancient Greeks held the first Olympic Games."),
    ("spirit","רוח","/ˈspɪrɪt/","noun","The spirit of the Olympics is about doing your best."),
    ("inspire","לעורר השראה","/ɪnˈspaɪər/","verb","Watching the Olympics inspired her to start gymnastics."),
]},

{
"title": "Healthy Eating",
"topic": "Health & Science",
"level": "intermediate",
"week": 14,
"text": """What we eat has a huge impact on how we feel, think, and perform every day. A healthy diet provides our bodies with the energy and nutrients they need to function properly. Fruits, vegetables, whole grains, and proteins are the building blocks of a balanced meal.

Many teenagers eat too much processed food — items like chips, fast food, and sugary drinks that are high in calories but low in nutritional value. Over time, poor eating habits can lead to health problems like obesity, diabetes, and heart disease.

Eating well does not have to be boring or expensive. Simple changes like drinking more water, eating a colorful variety of vegetables, and reducing sugar intake can make a big difference. Cooking your own meals is also a great way to understand exactly what you are putting into your body and to develop an important life skill.""",
"words": [
    ("nutrient","רכיב תזונתי","/ˈnjuːtriənt/","noun","Vegetables are full of vitamins and essential nutrients."),
    ("balanced","מאוזן","/ˈbæləns/","adjective","A balanced diet includes protein, carbohydrates, and healthy fats."),
    ("processed food","מזון מעובד","/ˈprɒsest fuːd/","noun","Processed food is often high in salt and sugar."),
    ("calorie","קלוריה","/ˈkæləri/","noun","Running burns a lot of calories."),
    ("obesity","השמנת יתר","/oʊˈbiːsɪti/","noun","Obesity is a growing health problem in many countries."),
    ("diabetes","סוכרת","/ˌdaɪəˈbiːtiːz/","noun","A poor diet can increase the risk of type 2 diabetes."),
    ("intake","צריכה","/ˈɪnteɪk/","noun","Reducing your salt intake is good for your heart."),
    ("protein","חלבון","/ˈproʊtiːn/","noun","Chicken, fish, and beans are excellent sources of protein."),
    ("variety","מגוון","/vəˈraɪəti/","noun","Eating a variety of foods gives your body all it needs."),
    ("impact","השפעה","/ˈɪmpækt/","noun","Your diet has a huge impact on your energy levels."),
    ("function","לתפקד","/ˈfʌŋkʃən/","verb","The brain needs glucose to function properly."),
    ("develop","לפתח","/dɪˈveləp/","verb","Cooking helps you develop useful life skills."),
]},

{
"title": "Robots and Artificial Intelligence",
"topic": "Technology",
"level": "intermediate",
"week": 15,
"text": """Robots and artificial intelligence, or AI, are rapidly changing the world around us. AI is the ability of a computer to perform tasks that normally require human intelligence, such as recognizing faces, understanding speech, or making decisions. Today, AI is already used in our smartphones, streaming services, and online shopping.

Robots are physical machines that can be programmed to carry out specific tasks. In factories, robots build cars and electronics with great speed and precision. In hospitals, robotic surgery allows doctors to perform delicate operations with incredible accuracy.

While AI and robots offer many exciting benefits, they also raise important questions. As more jobs become automated, many workers may find their skills no longer in demand. It is important that we teach the next generation to work alongside AI and to focus on creative, critical thinking skills that machines cannot easily replace.""",
"words": [
    ("artificial intelligence","בינה מלאכותית","/ˌɑːrtɪˈfɪʃəl ɪnˈtelɪdʒəns/","noun","Artificial intelligence is used to recommend videos online."),
    ("automated","אוטומטי","/ˈɔːtəmeɪtɪd/","adjective","The factory uses automated machines to build products."),
    ("precision","דיוק","/prɪˈsɪʒən/","noun","Robotic surgery is known for its incredible precision."),
    ("algorithm","אלגוריתם","/ˈælɡərɪðəm/","noun","Search engines use algorithms to find the best results."),
    ("recognize","לזהות","/ˈrekəɡnaɪz/","verb","Face recognition technology can recognize your face."),
    ("replace","להחליף","/rɪˈpleɪs/","verb","Some people worry that robots will replace human workers."),
    ("decision","החלטה","/dɪˈsɪʒən/","noun","AI can make complex decisions much faster than humans."),
    ("programmed","מתוכנת","/ˈproʊɡræmd/","adjective","Robots are programmed to carry out specific tasks."),
    ("delicate","עדין/מורכב","/ˈdelɪkɪt/","adjective","The surgeon performed a very delicate operation."),
    ("demand","ביקוש","/dɪˈmænd/","noun","There is a high demand for workers with coding skills."),
    ("critical thinking","חשיבה ביקורתית","/ˈkrɪtɪkəl ˈθɪŋkɪŋ/","noun","Critical thinking helps us evaluate information wisely."),
    ("rapidly","במהירות","/ˈræpɪdli/","adverb","Technology is developing rapidly every year."),
]},

{
"title": "Wildlife Conservation",
"topic": "Nature & Environment",
"level": "intermediate",
"week": 16,
"text": """Around the world, thousands of animal species are facing extinction due to human activities. Deforestation, illegal hunting, pollution, and climate change are destroying the natural habitats that wildlife depends on. Conservation organizations are working hard to protect these animals and the ecosystems they live in.

National parks and wildlife reserves play a crucial role in protecting animals. In these protected areas, animals can live and breed safely without the threat of hunters or habitat destruction. Scientists also work to protect endangered species through breeding programs in zoos and later releasing healthy animals back into the wild.

Every person can help with wildlife conservation. Reducing plastic use, supporting ethical wildlife tourism, and donating to conservation charities are all meaningful actions. Raising awareness is also important — the more people know about the problem, the more they will care about solving it.""",
"words": [
    ("extinction","הכחדה","/ɪkˈstɪŋkʃən/","noun","Many scientists warn that we are facing a mass extinction."),
    ("deforestation","כריתת יערות","/ˌdiːˌfɒrɪˈsteɪʃən/","noun","Deforestation destroys the homes of millions of animals."),
    ("illegal","לא חוקי","/ɪˈliːɡəl/","adjective","Illegal hunting has severely reduced elephant populations."),
    ("reserve","שמורת טבע","/rɪˈzɜːrv/","noun","The lions live safely inside the wildlife reserve."),
    ("breed","לרבות/לגדל","/briːd/","verb","The zoo has a program to breed endangered species."),
    ("release","לשחרר","/rɪˈliːs/","verb","The wolves were released back into the wild forest."),
    ("crucial","קריטי/חיוני","/ˈkruːʃəl/","adjective","Clean water is crucial for all living creatures."),
    ("awareness","מודעות","/əˈweənəs/","noun","Raising awareness about pollution is very important."),
    ("ethical","אתי","/ˈeθɪkəl/","adjective","Choose ethical tourism that respects local wildlife."),
    ("threat","איום","/θret/","noun","Climate change is a serious threat to polar bears."),
    ("protect","להגן","/prəˈtekt/","verb","We must protect rainforests before it is too late."),
    ("meaningful","משמעותי","/ˈmiːnɪŋfəl/","adjective","Volunteering is a meaningful way to help the environment."),
]},

# ═══════════════════════ ADVANCED (weeks 17-20) ═══════════════════════

{
"title": "Mental Health Awareness",
"topic": "Health & Society",
"level": "advanced",
"week": 17,
"text": """Mental health refers to our emotional, psychological, and social well-being. It affects how we think, feel, and behave — and it is just as important as physical health. Yet for many years, mental health was a topic surrounded by stigma, making it difficult for people who were struggling to seek help.

Today, awareness of mental health issues is growing, particularly among young people. Anxiety, depression, and stress are among the most common conditions affecting teenagers, often made worse by academic pressure, social media comparisons, and a lack of sleep. Recognizing the signs early and reaching out for support can make a significant difference.

Building mental resilience — the ability to adapt to and recover from difficult situations — is a key life skill. Practices such as mindfulness, regular exercise, maintaining strong social connections, and talking openly about feelings all contribute to better mental well-being. It is essential that schools and families create environments where young people feel safe to express themselves without judgment.""",
"words": [
    ("stigma","סטיגמה","/ˈstɪɡmə/","noun","There is still a stigma around talking about mental illness."),
    ("anxiety","חרדה","/æŋˈzaɪəti/","noun","Many students feel anxiety before important exams."),
    ("depression","דיכאון","/dɪˈpreʃən/","noun","Depression is a serious condition that requires professional help."),
    ("resilience","חוסן","/rɪˈzɪliəns/","noun","Resilience helps people recover after difficult experiences."),
    ("mindfulness","קשיבות/מיינדפולנס","/ˈmaɪndfəlnəs/","noun","Mindfulness practice can reduce stress and improve focus."),
    ("psychological","פסיכולוגי","/ˌsaɪkəˈlɒdʒɪkəl/","adjective","The accident had a lasting psychological impact on him."),
    ("acknowledge","להכיר/להודות","/əkˈnɒlɪdʒ/","verb","It is important to acknowledge your feelings without shame."),
    ("condition","מצב/מחלה","/kənˈdɪʃən/","noun","Anxiety is a common mental health condition in teenagers."),
    ("well-being","רווחה","/ˈwelˌbiːɪŋ/","noun","Exercise contributes to both physical and mental well-being."),
    ("judgment","שיפוט","/ˈdʒʌdʒmənt/","noun","A good friend listens without judgment."),
    ("contribute","לתרום","/kənˈtrɪbjuːt/","verb","A good diet and sleep contribute to better mental health."),
    ("essential","חיוני/הכרחי","/ɪˈsenʃəl/","adjective","It is essential to talk to someone when you feel overwhelmed."),
    ("seek","לחפש/לפנות","/siːk/","verb","Do not hesitate to seek help when you need it."),
    ("overwhelming","מכריע/מציף","/ˌoʊvərˈwelmɪŋ/","adjective","The pressure of exams can feel overwhelming sometimes."),
]},

{
"title": "Human Rights",
"topic": "Society & Ethics",
"level": "advanced",
"week": 18,
"text": """Human rights are the basic rights and freedoms that every person on Earth is entitled to, regardless of their nationality, gender, religion, or social status. The Universal Declaration of Human Rights, adopted by the United Nations in 1948, lists 30 fundamental rights, including the right to life, freedom of expression, education, and equality before the law.

Despite this declaration, millions of people around the world still suffer from violations of their basic rights. Poverty, discrimination, authoritarian governments, and armed conflicts continue to deny people their dignity and freedom. Women and minorities are particularly vulnerable to inequality and injustice in many parts of the world.

Defending human rights is not only the responsibility of governments — it is a duty that falls on every individual. Organizations like Amnesty International and Human Rights Watch monitor violations and advocate for victims globally. Young people today are increasingly using social media and activism to raise awareness and demand justice for those whose voices have been silenced.""",
"words": [
    ("fundamental","יסודי/בסיסי","/ˌfʌndəˈmentəl/","adjective","Freedom of speech is a fundamental right in democracies."),
    ("dignity","כבוד","/ˈdɪɡnɪti/","noun","Every person deserves to be treated with dignity."),
    ("discrimination","אפליה","/dɪˌskrɪmɪˈneɪʃən/","noun","Discrimination based on race or gender is illegal."),
    ("violation","הפרה","/ˌvaɪəˈleɪʃən/","noun","Torture is a serious violation of human rights."),
    ("authoritarian","אוטוריטרי","/ɔːˌθɒrɪˈteəriən/","adjective","The authoritarian government censored the press."),
    ("advocate","לתמוך/עורך דין","/ˈædvəkeɪt/","verb","She advocates for the rights of refugees."),
    ("equality","שוויון","/ɪˈkwɒlɪti/","noun","Equality before the law means everyone is judged the same."),
    ("vulnerable","פגיע","/ˈvʌlnərəbəl/","adjective","Children are among the most vulnerable members of society."),
    ("injustice","עוול/אי-צדק","/ɪnˈdʒʌstɪs/","noun","She dedicated her life to fighting injustice."),
    ("entitle","להעניק זכות","/ɪnˈtaɪtəl/","verb","Every citizen is entitled to a fair trial."),
    ("conflict","סכסוך","/ˈkɒnflɪkt/","noun","The armed conflict forced millions of people to flee."),
    ("monitor","לנטר/לעקוב","/ˈmɒnɪtər/","verb","International organizations monitor human rights violations."),
    ("silence","להשתיק","/ˈsaɪləns/","verb","Dictatorships try to silence journalists and critics."),
    ("activism","אקטיביזם","/ˈæktɪvɪzəm/","noun","Youth activism has driven major social changes throughout history."),
]},

{
"title": "The Future of Work",
"topic": "Technology & Society",
"level": "advanced",
"week": 19,
"text": """The nature of work is changing at an unprecedented rate. Automation, artificial intelligence, and globalization are reshaping entire industries, eliminating some jobs while creating entirely new ones. According to the World Economic Forum, nearly half of all current jobs may be significantly transformed or replaced by automation within the next decade.

This shift presents both challenges and opportunities. Workers in manufacturing, transportation, and data entry face the greatest threat from automation. However, professions that require creativity, emotional intelligence, complex problem-solving, and interpersonal skills are expected to remain in high demand.

Preparing for the future of work requires a new approach to education and lifelong learning. Rather than training for a single career, young people today must be flexible, continuously updating their skills as technology evolves. Concepts like remote work, the gig economy, and entrepreneurship are becoming increasingly central to how people earn a living.

The most important question is not whether technology will change our jobs — it certainly will — but whether individuals and societies are prepared to adapt.""",
"words": [
    ("automation","אוטומציה","/ˌɔːtəˈmeɪʃən/","noun","Automation has replaced many factory workers with robots."),
    ("unprecedented","חסר תקדים","/ʌnˈpresɪdentɪd/","adjective","The speed of technological change is unprecedented."),
    ("globalization","גלובליזציה","/ˌɡloʊbəlaɪˈzeɪʃən/","noun","Globalization has connected economies around the world."),
    ("eliminate","לבטל/להסיר","/ɪˈlɪmɪneɪt/","verb","New technology may eliminate millions of jobs worldwide."),
    ("entrepreneurship","יזמות","/ˌɒntrəprəˈnɜːrʃɪp/","noun","Entrepreneurship allows people to create their own businesses."),
    ("flexible","גמיש","/ˈfleksɪbəl/","adjective","A flexible worker can adapt to changing job requirements."),
    ("interpersonal","בינאישי","/ˌɪntərˈpɜːrsənəl/","adjective","Strong interpersonal skills are essential in any job."),
    ("lifelong learning","למידה לאורך חיים","/ˈlaɪflɒŋ ˈlɜːrnɪŋ/","noun","Lifelong learning is essential in a rapidly changing world."),
    ("gig economy","כלכלת ג'יג","/ɡɪɡ ɪˈkɒnəmi/","noun","The gig economy includes freelancers and short-term contractors."),
    ("evolve","להתפתח","/ɪˈvɒlv/","verb","Technology evolves so quickly that skills must be constantly updated."),
    ("transform","לשנות/לשנות צורה","/trænsˈfɔːrm/","verb","AI is transforming every industry from healthcare to education."),
    ("decade","עשור","/ˈdekeɪd/","noun","Technology has changed dramatically in the past decade."),
    ("professions","מקצועות","/prəˈfeʃənz/","noun","Professions like nursing require both skill and compassion."),
    ("adapt","להסתגל","/əˈdæpt/","verb","Workers must adapt to new technologies to stay relevant."),
]},

{
"title": "Fake News and Media Literacy",
"topic": "Society & Media",
"level": "advanced",
"week": 20,
"text": """In the digital age, information spreads faster than ever before — but so does misinformation. Fake news refers to deliberately false or misleading content presented as real news, designed to deceive readers and manipulate public opinion. The rise of social media has made it incredibly easy for false information to reach millions of people within hours.

Fake news can have serious real-world consequences. False health information during a pandemic can put lives at risk. Political misinformation can undermine democracy and fuel social division. In some cases, fake news has even incited violence.

Developing media literacy — the ability to critically evaluate information and identify reliable sources — is one of the most important skills in the modern world. Before sharing any news story, it is essential to check who wrote it, when it was published, and whether multiple trusted sources confirm the information.

Schools, governments, and technology companies all have a responsibility to combat misinformation. However, ultimately it is each individual's duty to think critically and resist the temptation to share content without first verifying its accuracy.""",
"words": [
    ("misinformation","מידע שגוי","/ˌmɪsɪnfəˈmeɪʃən/","noun","Misinformation about vaccines spread rapidly on social media."),
    ("deliberately","בכוונה","/dɪˈlɪbərɪtli/","adverb","The article was deliberately written to mislead readers."),
    ("manipulate","לתמרן/לשנות","/məˈnɪpjuleɪt/","verb","Politicians sometimes manipulate facts to gain support."),
    ("undermine","לחתור תחת","/ˌʌndəˈmaɪn/","verb","Fake news can undermine trust in democratic institutions."),
    ("incite","לגרות/להסית","/ɪnˈsaɪt/","verb","Dangerous online content can incite people to violence."),
    ("media literacy","אוריינות מדיה","/ˈmiːdiə ˈlɪtərəsi/","noun","Media literacy helps people identify reliable news sources."),
    ("verify","לאמת","/ˈverɪfaɪ/","verb","Always verify information before sharing it online."),
    ("credible","אמין","/ˈkredɪbəl/","adjective","Only share news from credible and verified sources."),
    ("bias","הטיה","/ˈbaɪəs/","noun","Every news source has some degree of political bias."),
    ("algorithm","אלגוריתם","/ˈælɡərɪðəm/","noun","Social media algorithms show content that keeps you engaged."),
    ("consequence","תוצאה/השלכה","/ˈkɒnsɪkwəns/","noun","Sharing false information can have serious consequences."),
    ("accuracy","דיוק","/ˈækjərəsi/","noun","Journalists must check the accuracy of every fact they report."),
    ("temptation","פיתוי","/tempˈteɪʃən/","noun","Resist the temptation to share news before checking it."),
    ("combat","להילחם ב-","/ˈkɒmbæt/","verb","Governments are trying to combat the spread of fake news."),
]},

]  # end LESSONS


def seed_data(db):
    """Seed users and lessons. Safe to call multiple times — skips existing."""
    for u in USERS:
        if not db.query(User).filter(User.username == u["username"]).first():
            db.add(User(username=u["username"], email=u["email"],
                        hashed_password=hash_password(u["password"]),
                        is_admin=u["is_admin"], level=u["level"]))
    db.commit()

    for data in LESSONS:
        if db.query(Lesson).filter(Lesson.title == data["title"]).first():
            continue
        lesson = Lesson(
            title=data["title"], topic=data["topic"], level=data["level"],
            week_number=data["week"], reading_text=data["text"], is_published=True,
        )
        db.add(lesson)
        db.flush()
        for w in data["words"]:
            db.add(Word(lesson_id=lesson.id, english=w[0], hebrew=w[1],
                        phonetic=w[2], word_type=w[3], example_sentence=w[4]))
    db.commit()


# Allow running directly: python seed_all.py
if __name__ == "__main__":
    create_tables()
    db = SessionLocal()
    seed_data(db)
    print("Seed complete: admin/admin123 | hallel/hallel123 | yair/yair123")
    db.close()
