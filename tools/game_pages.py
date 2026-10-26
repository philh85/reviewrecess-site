# -*- coding: utf-8 -*-
"""ALL THE WORDING FOR THE 13 GAME PAGES (/games/<slug>/). Edit here, then run:  py tools\\build.py
Plain text only: build.py escapes it (so "&" and "<" are safe to type). Keep it true to the game.

Rules for this file
* No prices. No other companies' trademarks in titles (no TV-show or board-game brand names anywhere).
* "Answer Armada" is never shortened to "Armada", and never called "Battleship".
* Word Magnets and Sentence Snap are always written with "Review Recess" in front.
* US English.

Each game has:
  slug, name, short, tag, grades, subjects, players, time   -> the "At a glance" box
  title (browser tab / Google result, keep under ~65 characters), description (~150 characters), h1
  intro: 1-3 short paragraphs
  setup / round / scoring: the numbered "How to play" steps
  modes: [(name, text)]  settings: [(name, text)]  tips: [text]  subject_ideas: {subject: text}
         Add FULL as a third item, e.g. (name, text, FULL), to show a small "Full version" badge on that feature.
  free_extra: one extra line in the Free version card on what is NOT in the free version ("" = none)
  full_extra: one extra line on what the full version adds for THIS game ("" = none)
  faq: [(question, answer)]  (3-6; also becomes FAQPage schema)
  shots: [(image key, source png under /workspace, alt text, caption)]  -> tools/make_images.py
         The first shot is the main image (also used on the Games and Home pages).
  related: 3 slugs
"""

# Shared blocks used on every page -------------------------------------------------------------
NEED = [
    ("A Google account", "The full version runs in your own Google account and saves your question banks in a Google Sheet in your Drive. A personal account works if your school blocks the games."),
    ("A computer with an up-to-date browser", "Chrome works best. There's nothing to install, no copy to make and no script editor to open."),
    ("A projector, smart TV or interactive board", "Everything the class needs is on one screen. Students don't need accounts or devices."),
]
FREE_TEXT = ("The free version is the complete game with one fixed sample set built in. You can play it straight away "
             "and tick or untick which items to use, but you can't edit the set or add your own.")
FULL_TEXT = ("The full version lets you add, paste and edit as many question banks as you like. They're saved in a Google Sheet "
             "in your own Google Drive, so you can reuse them every year. Saved class rosters and the fair student picker are included too.")
BUNDLE_TEXT = ("The all-access bundle includes the full version of every game plus every Review Recess question pack, "
               "including new packs as they're added.")

FULL = "full"   # marks a mode or setting as full version only (gold "Full version" badge)

GAME_PAGES = []

# =============================================================================================
GAME_PAGES.append(dict(
 slug="answer-armada", name="Review Recess Answer Armada", short="Answer Armada", tag="Whole class vs teacher",
 grades="Grades 2–12 (picture styles for K–6 and 7–12)", subjects="Any subject", players="The whole class against the teacher",
 time="15–30 minutes",
 title="Answer Armada: Hidden-Ships Review Game | Review Recess",
 description="A whole-class review game for any subject: every correct answer earns one shot at the teacher's hidden ships. Three difficulty levels and six picture styles.",
 h1="Answer Armada: a hidden-ships review game where every right answer earns a shot",
 intro=[
  "Review Recess Answer Armada turns any question set into a team mission. The whole class plays together against the teacher. A correct answer earns exactly one shot at a lettered and numbered grid, and the class has to find and sink every hidden ship before the shots run out.",
  "It works for any subject, from early elementary to high school. Younger classes can hunt for dinosaurs, eggs or animals instead of ships, and older classes get the Classic Fleet.",
 ],
 setup=[
  "Open the game and choose a picture style: Classic Fleet (Grades 7–12) or one of five K–6 styles: Sea Safari, Dino Dig, Space Explorer, Spring Egg Hunt or Jungle Safari.",
  "Pick a difficulty. Easy is a 7 × 5 grid with 5 ships and 28 shots, Normal is 7 × 5 with 3 ships and 21 shots, and Hard is a bigger 9 × 7 grid with 3 ships and 28 shots.",
  "Choose a question bank (or use the general review sample), and use ☑ Choose… to untick any questions you don't want today. You can also hide the questions and ask your own out loud.",
  "Press Start game and go full screen. The ships are placed at random every game.",
 ],
 round=[
  "Press Next question. The question appears as the largest text on the screen, and the grid stays locked (🔒) until you mark the answer.",
  "Call on a student (or use 🎤 Pick a student) to answer. Press Show answer if you want the class to see it.",
  "Press ✓ Correct to unlock the grid for exactly one shot. Press ✗ Incorrect to show the answer and move on with no shot.",
  "The class calls a square, such as C4, and you click it. The game shows a miss, a hit or a sunk ship. Extra clicks are ignored, and the next question comes up by itself with the grid locked again.",
 ],
 scoring=[
  "A hit shows only a neutral marker, so nobody can tell which ship it was. A ship's full picture appears only when every square of it has been found.",
  "The scoreboard tracks shots left, hits with accuracy, ships still afloat and the level.",
  "If the class sinks every ship, the class wins. If the shots run out first, the teacher survives and the hidden ships are shown.",
 ],
 modes=[
  ("Classic Fleet (Grades 7–12)", "Navy ships on a sea grid. This is the default style."),
  ("Five K–6 picture styles", "Sea Safari, Dino Dig, Space Explorer, Spring Egg Hunt and Jungle Safari. The rules stay the same. Only the pictures, wording and sounds change."),
  ("Easy, Normal and Hard", "More ships make Easy friendlier. Hard uses a bigger grid, so every shot counts."),
 ],
 settings=[
  ("Question banks", "Use the samples (General review and Grammar review) or your own banks, and tick exactly which questions to use."),
  ("Hide questions", "Hide the question card and read your own questions aloud, which is handy for quick oral review."),
  ("Sound on or off", "Short sound effects for misses, hits and sunk ships. Turn them off from setup or the teacher bar."),
  ("Display options", "Light, dark and high-contrast themes, bigger text and larger buttons for the projector."),
 ],
 tips=[
  "Let a different student call the square each time, so the whole room is involved even when one student answers.",
  "Use 🎤 Pick a student for fair turns. Everyone gets a go before anyone repeats.",
  "Differentiate with difficulty: Easy for a quick win at the end of a lesson, Hard for a longer test-prep session.",
  "Press Show fleet at the end and talk about which squares would have been better guesses.",
 ],
 subject_ideas={
  "Math": "Multiplication facts, equivalent fractions, order of operations, unit conversions.",
  "ELA": "Grammar terms, vocabulary definitions, figurative language, story elements.",
  "Science": "States of matter, body systems, food chains, lab safety.",
  "Social studies": "State capitals, map skills, branches of government, timeline events.",
 },
 full_extra="",
 faq=[
  ("Can students fire more than one shot per question?", "No. The grid is locked while a question is up. ✓ Correct unlocks it for exactly one square, even if students click several squares quickly, and ✗ Incorrect gives no shot. An unused shot never carries over to the next question."),
  ("Is it suitable for kindergarten and lower elementary?", "Yes. Five picture styles (Sea Safari, Dino Dig, Space Explorer, Spring Egg Hunt and Jungle Safari) are made for Grades K–6. The questions are up to you, so you can keep them as simple as you need."),
  ("Can I use it without a question bank?", "Yes. Press Hide questions and ask your own questions out loud. Press Next question for each one, then ✓ Correct or ✗ Incorrect as usual. A correct answer still earns exactly one shot."),
  ("How long does a game take?", "It depends on the difficulty and how quickly you move through questions. Normal has 21 shots, so a game usually fits into one review session."),
 ],
 shots=[
  ("answer-armada", "marketing/armada-themes/fleet-2-midgame.png", "Answer Armada in play: a large question on the left and a lettered, numbered grid with hit and miss markers on the right, with the scoreboard above.", "The Classic Fleet style. The question is the biggest thing on the screen."),
  ("answer-armada-sea", "marketing/armada-themes/sea-2-midgame.png", "Answer Armada in the Sea Safari style for younger classes, with sea animals to find instead of ships.", "Sea Safari, one of five K–6 picture styles."),
  ("answer-armada-dino", "marketing/armada-themes/dino-3-found-reveal.png", "Answer Armada in the Dino Dig style, with a fully found dinosaur revealed across its squares.", "Dino Dig: a picture appears only when it has been completely found."),
  ("answer-armada-setup", "marketing/armada-themes/fleet-1-setup.png", "The Answer Armada setup screen with six picture styles, three difficulty levels and the question bank.", "Setup: pick a picture style, a difficulty and your questions."),
 ],
 related=["brain-board-blitz", "tic-tac-toe-quiz-game", "million-point-climb"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="brain-board-blitz", name="Brain Board Blitz", short="Brain Board Blitz", tag="Quiz board",
 grades="Grades 3–12", subjects="Any subject · Unit and test review", players="2 or more teams",
 time="20–45 minutes",
 title="Brain Board Blitz: Quiz Board Review Game | Review Recess",
 description="A 5 × 5 game-show style quiz board for team review in any subject, with 1–5 rounds, a timer, skip limits, live scores and saved games you can resume.",
 h1="Brain Board Blitz: a game-show style quiz board for team review in any subject",
 intro=[
  "Brain Board Blitz is a classic five-category quiz board for the front of the room. Teams take turns choosing a category and a point value, a student answers against an optional timer, and the scores update live.",
  "Use it for end-of-unit and test review in any subject from Grades 3 to 12. Play one round or up to five. With the full version, you can save the game and finish it next lesson.",
 ],
 setup=[
  "Choose a question set and a class roster. The board needs five complete categories, each with questions at levels 1 to 5.",
  "Pick the number of rounds (1–5) and the Round 1 point values (1–5, 10–50, 100–500 or 200–1000). Each later round adds a step: Round 2 is double Round 1, Round 3 is triple, and so on.",
  "Set the skips per team (unlimited or 1–5), then press Start game. You need at least two active teams.",
 ],
 round=[
  "The team in control picks a category and a value. The question opens in a large window.",
  "Press 🎲 Pick to choose a student from that team. The picker is fair, so everyone gets a turn before anyone repeats.",
  "Start the timer if you want one (10, 20, 30, 45 or 60 seconds), then press 👁 Reveal answer.",
  "Mark the answer ✓ Correct, ✕ Incorrect, or Skip / no points. Used squares are marked on the board.",
  "When every square is used, press ⏭ Next round. Later rounds use questions you haven't played yet.",
 ],
 scoring=[
  "A correct answer adds the points, and the team keeps control.",
  "An incorrect answer takes the points away, and control passes to the next team.",
  "Skip / no points uses one of that team's skips. You can still fix any score with the − / + buttons, and ↶ Undo reverses the last answer.",
  "The team with the most points after the last round wins.",
 ],
 modes=[
  ("1 to 5 rounds", "A quick one-round game or a longer tournament. Point values grow each round."),
  ("Skip limits", "Unlimited skips, or 1–5 per team for the whole game, so teams can't skip every hard question."),
  ("Save and resume", "The game saves itself after every answer. Pick it up next lesson with 📂 Resume a saved game.", FULL),
 ],
 settings=[
  ("Point values", "1–5, 10–50, 100–500 or 200–1000 for Round 1."),
  ("Timer", "Optional: 10, 20, 30, 45 or 60 seconds, with a sound at zero."),
  ("Question library", "Load, save and delete sets, add questions by category and level, import or export CSV, or paste rows from Google Sheets. A readiness check shows any missing category or level."),
  ("Team rosters", "Paste one student per line as Team, Student, and untick absent students after loading."),
 ],
 tips=[
  "Write level 1 questions everyone can answer, and save level 5 for stretch questions. That gives every student a chance to score.",
  "Set skips to 1 or 2 per team so teams try the harder squares instead of passing.",
  "Use the timer for older classes, and turn it off for younger students or English learners.",
  "With the full version, play Round 1 one day and resume the saved game the next for a two-day review.",
 ],
 subject_ideas={
  "ELA": "Categories for vocabulary, grammar, literary devices, authors and genres.",
  "Math": "Categories for fractions, geometry, word problems, measurement and mental math.",
  "Science": "Categories for cells, ecosystems, forces, the water cycle and lab safety.",
  "Social studies": "Categories for U.S. geography, civics, key people, events and vocabulary.",
 },
 full_extra="Save and resume is full version only: the game saves itself after every answer, and saved games are kept in the browser and in the Games tab of your own question spreadsheet.",
 free_extra="Save and resume, for finishing a game next lesson, is in the full version.",
 faq=[
  ("How many questions do I need?", "One question for each of the 5 categories at each of the 5 levels (25 in all) for one round. For more rounds, add more per category and level. The readiness check shows exactly what's missing."),
  ("Can I stop and finish the game next lesson?", "Yes, in the full version. The game saves itself after every answer, and 💾 Save saves it whenever you like. Next lesson, choose 📂 Resume a saved game. Save and resume isn't included in the free version."),
  ("Can I correct a mistake?", "Yes. ↶ Undo reverses the last answer, and every team score has − / + buttons."),
  ("How many teams can play?", "At least two. Teams come from your class roster, and you can untick absent students."),
 ],
 shots=[
  ("brain-board-blitz", "marketing/bbb-redesign/after-v2.5-board-1600x900.png", "Brain Board Blitz board: five categories across the top, point values from 100 to 500 below, and team scores above the board.", "The 5 × 5 board with live team scores."),
  ("brain-board-blitz-question", "marketing/bbb-redesign/after-v2.5-question-1600x900.png", "A Brain Board Blitz question in large text with buttons to reveal the answer and mark it correct or incorrect.", "Each question opens in a big, readable window."),
  ("brain-board-blitz-setup", "marketing/bbb-redesign/after-v2.5-setup-1600x900.png", "Brain Board Blitz teacher setup with question set, roster, number of rounds, point values and skips per team.", "Setup: rounds, point values and skips per team."),
  ("brain-board-blitz-win", "marketing/bbb-redesign/after-v2.5-win-settled-1600x900.png", "Brain Board Blitz final scores with the winning team at the top.", "Final scores at the end of the game."),
 ],
 related=["million-point-climb", "tic-tac-toe-quiz-game", "answer-armada"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="million-point-climb", name="Million Point Climb", short="Million Point Climb", tag="Quiz show",
 grades="Grades 4–12", subjects="Any subject", players="One contestant at a time, with the whole class following along",
 time="5–10 minutes per contestant",
 title="Million Point Climb: Quiz Show Review Game | Review Recess",
 description="A multiple-choice quiz show for your classroom: students climb a points ladder with lifelines and safety nets. Run it on one screen or with a separate TV display.",
 h1="Million Point Climb: a climb-the-ladder quiz show review game for your classroom",
 intro=[
  "Million Point Climb is a multiple-choice quiz show for the front of the room, like the TV quiz shows students know. One contestant at a time climbs a points ladder, with lifelines, safety nets and the option to walk away.",
  "Students answer out loud, so no student devices are needed. It suits Grades 4–12 in any subject, and the questions can get harder as the ladder climbs.",
 ],
 setup=[
  "Choose how to run it. Basic uses one screen: the question fills the screen, and a slim teacher bar sits along the bottom. Presenter (full version) gives you a clean Display for the TV and a private Controller on your laptop (or phone) that shows you the answer.",
  "Highlight one or more question sets and add them to the session. Each question has four choices, and can also have a difficulty, a category, a hint and an explanation.",
  "Check the class session settings: the prize ladder, the prize prefix, the safety-net questions and the lifelines. Add your students, one name per line.",
  "Press Start new class session.",
 ],
 round=[
  "Choose the next contestant. Each student plays one climb per class session.",
  "Read the question. The contestant picks an answer, and you select it.",
  "Press the main button to step through Lock in, then Reveal, then Next question. It's one button, so you can't press the wrong one.",
  "The contestant can use each lifeline once: 50:50, Ask the Audience, Phone a Friend, Switch the question and Ask the Host.",
  "The contestant can walk away with their points, or keep climbing.",
 ],
 scoring=[
  "Each correct answer moves the contestant up the ladder. The ladder shows the current points and the guaranteed amount.",
  "Safety-net questions (questions 5 and 10 by default) lock in points, so a wrong answer later drops the contestant back to the last safety net.",
  "A results table records each contestant's name, points and outcome for the session.",
 ],
 modes=[
  ("Basic: one screen", "Best for one laptop on the projector. The show fills the screen, with a slim teacher bar and keyboard shortcuts."),
  ("Presenter: Display + Controller", "Open the Display on the TV or an extended screen. Your Controller is the only screen that shows the correct answer.", FULL),
  ("Phone remote", "In Presenter mode, open the same game link on your phone, signed in to the same Google account, and enter the 4-digit code from the Display. Expect a 1–3 second delay per tap, and keep the laptop window open.", FULL),
  ("Fastest Finger First", "An optional ordering round to choose the next contestant. Students write the order on paper, and the game shows the correct order."),
 ],
 settings=[
  ("Prize ladder", "Your own list of 5–30 rising values, with a prize prefix ($ by default)."),
  ("Safety nets", "Choose which question numbers lock in points."),
  ("Lifelines", "Ask the Audience is simulated on screen. Phone a Friend can be a real classmate or a simulated friend, with 30 seconds. Ask the Host uses each question's hint and can be turned off."),
  ("Increasing difficulty", "Questions get harder as the ladder climbs, using the difficulty levels in your question sets."),
 ],
 tips=[
  "Have the class answer on mini whiteboards while the contestant thinks, so everyone works on every question.",
  "Use the real-classmate option for Phone a Friend, so a second student gets to explain their thinking.",
  "Add a short explanation to each question and read it out after Reveal to turn mistakes into teaching moments.",
  "Play a short Fastest Finger First round to pick contestants fairly.",
 ],
 subject_ideas={
  "Science": "Vocabulary, steps in a process, units of measurement, scientists and discoveries.",
  "Math": "Estimation, mental math and word problems with four answer choices.",
  "ELA": "Vocabulary in context, grammar choices, literary terms, author's purpose.",
  "Social studies": "Key events, people, documents and map questions.",
 },
 full_extra="Presenter mode is full version only: a clean Display for the TV, a private Controller on your laptop and the phone remote.",
 free_extra="The free version runs in Basic mode on one screen. Presenter mode (TV Display, Controller and phone remote) is in the full version.",
 faq=[
  ("Do students need devices?", "No. Students answer out loud, and the whole game runs on your screen."),
  ("Is Presenter mode in the free version?", "No. The free version runs in Basic mode on one screen. Presenter mode, with the TV Display, the private Controller and the phone remote, is full version only."),
  ("How do I show the questions on the TV but keep the answer on my laptop?", "Use Presenter mode, which is in the full version. Choose Presenter, press Open Display and drag that window to the TV or extended screen. Your laptop becomes the Controller, the only screen that shows the correct answer."),
  ("Can I use my phone as a remote?", "Yes, with the full version, in Presenter mode. Open the game link on your phone, signed in to the same Google account as the laptop, and enter the 4-digit code from the Display. Each tap takes about 1–3 seconds to reach the Display."),
  ("Do questions repeat?", "Not within a class session until the questions are reshuffled. Starting a new class session clears the history and lets every student play again."),
 ],
 shots=[
  ("million-point-climb", "marketing/mpc-redesign/after-v2.5-basic-game-1600x900.png", "Million Point Climb in Basic mode: a large question with four answer choices and the points ladder on the right.", "Basic mode: the question fills the screen, with a slim teacher bar."),
  ("million-point-climb-display", "marketing/mpc-redesign/after-v2.5-display-question-1920x1080.png", "The Million Point Climb Display for the TV, showing a question and four answers with no teacher controls.", "Presenter mode: the Display for the TV has no controls."),
  ("million-point-climb-controller", "marketing/mpc-redesign/after-v2.5-controller-desktop-1440x900.png", "The Million Point Climb Controller on the teacher's laptop, showing the question, the marked correct answer and the lifeline buttons.", "The Controller is the only screen that shows the answer."),
  ("million-point-climb-audience", "marketing/mpc-redesign/after-v2.5-lifeline-audience-1600x900.png", "The Ask the Audience lifeline in Million Point Climb, with a bar chart of votes above the question.", "Lifelines include Ask the Audience and 50:50."),
 ],
 related=["brain-board-blitz", "answer-armada", "tic-tac-toe-quiz-game"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="forbidden-words", name="Forbidden Words", short="Forbidden Words", tag="Vocabulary speaking game",
 grades="Grades 5–12", subjects="Vocabulary in any subject", players="2–10 teams, or 2–20 pairs",
 time="15–40 minutes",
 title="Forbidden Words: Vocabulary Guessing Game | Review Recess",
 description="Students explain a key term without saying the forbidden words while the class guesses. Team and pair modes, a timer and fair turns for vocabulary review.",
 h1="Forbidden Words: a vocabulary game where students explain without the forbidden words",
 intro=[
  "Forbidden Words is a speaking game for vocabulary review. A student explains the word on the card without saying any of the forbidden words underneath it, while the class tries to guess it before the timer runs out.",
  "Because students have to explain ideas in their own words, it's great for academic vocabulary in any subject. It suits Grades 5–12 and works with 2–10 teams or 2–20 pairs.",
 ],
 setup=[
  "Choose Team mode or Pair mode.",
  "Choose a card deck. Each card is a word plus its forbidden words.",
  "Set the round length (30, 45, 60, 90 or 120 seconds), what happens when someone calls \"Forbidden!\", and who guesses.",
  "Enter your teams and students (or load a roster), or set up your pairs, then press ▶ Start competition.",
 ],
 round=[
  "Choose which team goes next and tap a student to come up and explain. The next student in rotation is suggested.",
  "Press Start. The student explains the word on the card without saying it or any of the \"Don't say\" words.",
  "Press ✔ Correct when someone guesses it, ⏭ Pass to skip the card, or 🚫 Forbidden! if a forbidden word slips out.",
  "When time runs out, the Time's up screen shows how many cards were correct, passed and forbidden. Press Next for the next team.",
 ],
 scoring=[
  "Each correct guess is +1 for the explainer's team (or pair).",
  "\"Forbidden!\" follows your setting: skip the card with no penalty (the default), −1 for the explaining side, or +1 for the team that called it.",
  "↶ Undo fixes a mis-tap. 🏆 Scoreboard shows the team scoreboard or the pair leaderboard at any time.",
 ],
 modes=[
  ("Team mode", "Call students up one at a time. The whole class guesses, and the points go to the student's team."),
  ("Pair mode", "Partners come to the screen in turn. One explains and the other guesses, and they swap next time. The class watches for forbidden words."),
  ("Who guesses", "The whole class (points still go to the explainer's team) or only the explainer's team."),
 ],
 settings=[
  ("Round length", "30, 45, 60, 90 or 120 seconds."),
  ("Forbidden penalty", "No penalty, −1 for the explaining side, or +1 for the team that called it."),
  ("Fixed-size card", "The word, the forbidden words, the timer and the buttons stay in the same place whether a card has one line or two."),
  ("Saved competition", "The competition is saved in the browser, so you can resume it next lesson."),
 ],
 tips=[
  "Model one card yourself first, so students hear what a good explanation sounds like.",
  "For younger students or English learners, use fewer forbidden words and a longer round.",
  "Make one student per team the forbidden-word judge to keep the whole class listening.",
  "Afterward, ask students to write a definition for any card that was passed.",
 ],
 subject_ideas={
  "Science": "Photosynthesis, erosion, gravity or ecosystem, with forbidden words like plant, sun or water.",
  "Social studies": "Democracy, treaty, migration, amendment.",
  "ELA": "Literary terms such as metaphor, protagonist and theme.",
  "Math": "Perimeter, denominator, parallel, variable.",
 },
 full_extra="",
 faq=[
  ("Does a team lose a point for saying a forbidden word?", "Only if you choose that. The default skips the card with no penalty. You can also choose −1 for the explaining side, or +1 for the team that called it."),
  ("Can students play in pairs instead of teams?", "Yes. Pair mode takes 2–20 pairs. Partners take turns explaining and guessing, with a pair leaderboard."),
  ("How do I choose who comes up?", "Before each turn, tap a student's name. The next student in rotation is suggested, so everyone gets a turn."),
  ("Are there keyboard shortcuts?", "Yes: C for correct, P for pass, F for forbidden, Space to pause and Ctrl/⌘+Z to undo."),
 ],
 shots=[
  ("forbidden-words", "marketing/fw-redesign/after/after-v2.5-light-1600x900-3-game-short.png", "Forbidden Words card for the word Treaty with three forbidden words, a countdown timer and Correct, Pass and Forbidden buttons.", "A round in progress: explain the word without the forbidden ones."),
  ("forbidden-words-lobby", "marketing/fw-redesign/after/after-v2.5-light-1600x900-2-lobby.png", "The Forbidden Words lobby asking a volunteer from Team 1 to come up, with the team's student names to tap.", "Before each turn, tap the student who comes up."),
  ("forbidden-words-setup", "marketing/fw-redesign/after/after-v2.5-light-1600x900-1-setup.png", "Forbidden Words setup with Team mode and Pair mode, the card deck and the round settings.", "Setup: team or pair mode, deck, round length and penalty."),
  ("forbidden-words-scoreboard", "marketing/fw-redesign/after/after-v2.5-light-1600x900-6-scoreboard.png", "The Forbidden Words team scoreboard with a podium for the top three teams.", "The team scoreboard."),
 ],
 related=["five-second-battle", "pass-the-bomb", "mystery-cat"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="letter-lifeline", name="Letter Lifeline", short="Letter Lifeline", tag="Spelling & vocabulary",
 grades="Grades 1–12 (Classic pictures for K–6, Skeleton for 7–12)", subjects="Spelling and vocabulary in any subject", players="1 vs 1, 2–4 teams (up to 6 from a roster), or the whole class",
 time="10–30 minutes",
 title="Letter Lifeline: Spelling Word Guessing Game | Review Recess",
 description="A picture-based alternative to hangman for spelling and vocabulary. Guess the letters before the picture runs out, with clues, 20 themes and team scoring.",
 h1="Letter Lifeline: a picture-based alternative to hangman for spelling and vocabulary",
 intro=[
  "Letter Lifeline is a guess-the-letters word game with friendly pictures instead of a gallows. Every wrong letter takes a visible piece away from the picture, and the class has to find the word before it's gone.",
  "Use it for spelling lists or unit vocabulary from Grades 1–12. An optional clue line under each word turns guessing into recall practice. Play 1 vs 1, in teams or as a whole class.",
 ],
 setup=[
  "Choose the game mode: 1 vs 1, Teams (2, 3 or 4, or up to 6 from a roster) or Whole Class.",
  "Choose the game length: Quick (6), Standard (10), Epic (15) or Mega (20) wrong guesses.",
  "Choose a picture style: Classic (K–6), with 20 themes or 🎲 Surprise me, or Skeleton (7–12), a classroom anatomy model.",
  "Set the options (💡 Hints and 🏅 Auto-award points, each on or off), choose your word bank and press START GAME.",
 ],
 round=[
  "The word appears as blanks. Spaces, hyphens and symbols are shown, and only the letters are hidden.",
  "The player or team guesses a letter, and you click it on the on-screen A–Z buttons. Correct letters turn green and wrong ones turn red.",
  "A correct letter keeps the turn. A wrong letter removes a piece of the picture and passes the turn to the next player or team.",
  "If a team thinks it knows the word, press 💡 Guess the answer and mark it ✓ Correct or ✗ Incorrect.",
  "Press Next word ➜ when the word is solved or the picture runs out.",
 ],
 scoring=[
  "With Auto-award on, whoever guesses the last letter gets +1, and the message names the scorer.",
  "Guess the answer: a correct guess is +2 and solves the word, and an incorrect guess is −1 and passes the turn.",
  "👁 Reveal shows the answer with no points. Every scoreboard card has −1 / +1 buttons, and ↶ Undo steps back one letter.",
  "Press 🏁 End game for the final scores.",
 ],
 modes=[
  ("1 vs 1, Teams or Whole Class", "Head-to-head, 2–4 teams (up to 6 from a roster), or the whole class against the picture."),
  ("Classic pictures (K–6)", "20 themes, such as a pizza, a snowman and a rocket, or 🎲 Surprise me for a new theme every word."),
  ("Skeleton (Grades 7–12)", "A classroom anatomy model loses a bone or part with each wrong guess and topples over when the guesses run out."),
  ("Game length", "6, 10, 15 or 20 wrong guesses. Every wrong letter visibly changes the picture at every length."),
 ],
 settings=[
  ("Hints", "On shows the word bank's clue under the word. Off hides it for a harder game."),
  ("Auto-award points", "On gives +1 to whoever guesses the last letter. Off leaves scoring to you."),
  ("Word banks", "Words with optional clues, such as the River Valley Civilizations sample."),
  ("Reduced motion", "The pictures follow the light, dark and high-contrast themes and respect your computer's reduce-motion setting."),
 ],
 tips=[
  "Write each clue as a definition, so students practice meaning as well as spelling.",
  "Turn Hints off for a second play-through of the same list.",
  "Use Whole Class mode for younger students, and Teams with Auto-award for competitive older classes.",
  "Pick Quick (6) for a challenge, or Mega (20) to give younger classes more chances.",
 ],
 subject_ideas={
  "ELA": "Weekly spelling words, vocabulary from a novel, prefixes and suffixes.",
  "Science": "Key terms with definitions as clues: habitat, condensation, magnet.",
  "Social studies": "People, places and terms from the unit, such as Mesopotamia or pharaoh.",
  "Math": "Math vocabulary: perimeter, quotient, parallelogram.",
 },
 full_extra="",
 faq=[
  ("Is this a hangman game?", "It plays like the classic letter-guessing game, but with friendly pictures instead of a gallows. Each wrong letter takes a piece away from a pizza, a snowman, a rocket and more, or from a skeleton model for older students."),
  ("Can I hide the clue?", "Yes. Turn Hints off on the setup screen to hide the clue line in every mode."),
  ("Does every wrong guess change the picture?", "Yes, at every game length. Each picture is split to match the number of wrong guesses you choose."),
  ("Does it store student scores?", "No. Letter Lifeline doesn't save scores or student data."),
 ],
 shots=[
  ("letter-lifeline", "v2-screenshots/v2.4/letter-lifeline-light-penguin-play-1920x1080.png", "Letter Lifeline in play: a penguin picture on the left, a partly revealed word with a clue, A–Z letter buttons and team scores.", "A Classic picture theme, with the clue under the word."),
  ("letter-lifeline-skeleton", "v2-screenshots/v2.5/ll-skel-light-play.png", "The Letter Lifeline Skeleton style for older students: an anatomy model on a stand next to the word and the letter buttons.", "The Skeleton style for Grades 7–12."),
  ("letter-lifeline-setup", "v2-screenshots/v2.5/ll-setup-classic-full.png", "Letter Lifeline setup with game mode, game length, picture style, picture themes and the Hints and Auto-award options.", "Setup: mode, length, picture style and options."),
  ("letter-lifeline-win", "v2-screenshots/v2.4/letter-lifeline-dark-rocket-win-1920x1080.png", "Letter Lifeline in the dark theme, with a rocket picture and a solved word.", "A solved word in the dark theme."),
 ],
 related=["word-scramble", "mystery-cat", "sentence-snap"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="pass-the-bomb", name="Pass the Bomb", short="Pass the Bomb", tag="Speaking warm-up",
 grades="Grades K–12 (jack-in-the-box, bear and baby styles for younger kids)", subjects="Speaking, vocabulary and quick review", players="The whole class, in a circle or in rows",
 time="5–15 minutes",
 title="Pass the Bomb: Hot Potato Speaking Game for Class | Review Recess",
 description="A hot-potato speaking warm-up: answer the prompt and pass before the hidden timer goes off. Bomb, jack-in-the-box, sleeping bear and sleeping baby styles.",
 h1="Pass the Bomb: a hot-potato speaking game for quick classroom warm-ups",
 intro=[
  "Pass the Bomb is a fast speaking warm-up. Students answer a prompt and pass an object (or the turn) to the next person before the hidden timer goes off. Nobody knows when that will happen, so answers stay short and the room stays focused.",
  "Choose the classic bomb for older students, or a jack-in-the-box, a sleeping bear or a sleeping baby for younger kids. It works with the whole class and needs nothing but your screen and something to pass.",
 ],
 setup=[
  "Choose a picture style: 💣 Bomb (BOOM!), Jack-in-the-box (POP!), Sleeping bear (ROAR!) or Sleeping baby (WAAH!).",
  "Choose the game mode: Category Mode (the same prompt all round) or Rapid Prompt Mode (a new prompt after every pass).",
  "Set the shortest and longest time. It goes off at a random moment between them, anywhere from 10 to 60 seconds.",
  "Choose your prompts (one per line, or a saved prompt bank), the prompt order and the sound, then press ▶ START GAME.",
 ],
 round=[
  "Press ▶ START. The prompt appears in a fixed box above the picture.",
  "The first student answers the prompt and passes the object to the next student.",
  "Press PASS! ▸ after each pass. In Rapid Prompt Mode, the next student gets a new prompt and the clock keeps running.",
  "The picture looks the same the whole time, so nothing gives the end away. Then it goes off: BOOM!, POP!, ROAR! or WAAH!",
 ],
 scoring=[
  "No points are kept. It's a speaking game, and the fun is in not being the one holding it.",
  "The result screen shows the picture, asks \"Who was holding the bomb?\" (or \"Who woke the bear?\") and shows the number of passes.",
  "Press NEXT ROUND → to go again, or ⚙ SETUP to change the prompts.",
 ],
 modes=[
  ("Category Mode", "Everyone answers the same prompt until it goes off, for example \"Name a mammal\"."),
  ("Rapid Prompt Mode", "A new prompt after every pass, for quick-fire review."),
  ("Four picture styles", "A bomb for older classes, and a jack-in-the-box, a sleeping bear and a sleeping baby for younger kids."),
 ],
 settings=[
  ("Shortest and longest time", "Shortest 10–30 seconds, longest 20–60 seconds. The exact moment is random and hidden."),
  ("Prompt order", "Random or in order."),
  ("Sound on or off", "Each style has its own idle sound and ending."),
  ("Keyboard", "Space to start, → or P to pass, N for a new prompt and X to stop."),
 ],
 tips=[
  "Use a soft ball or a beanbag as the object to pass.",
  "For younger students, use a longer time range and the jack-in-the-box, bear or baby.",
  "In Category Mode, don't count repeated answers. It pushes students to recall more.",
  "Use 🎲 New prompt if a category turns out too hard or too easy.",
 ],
 subject_ideas={
  "Math": "Say a multiple of 5, name a shape, say a number bigger than 100.",
  "ELA": "Name a noun, say an action verb, say a word that rhymes with cat.",
  "Science": "Name a mammal, name a planet, name something that is a solid.",
  "Social studies": "Name a U.S. state, name a continent, name a community helper.",
 },
 full_extra="",
 faq=[
  ("Can students tell when it will go off?", "No. It goes off at a random moment between your shortest and longest time, and the picture and sound stay the same all round."),
  ("Is there a version for younger kids?", "Yes. Choose the jack-in-the-box, the sleeping bear or the sleeping baby instead of the bomb."),
  ("Does it keep score?", "No. It's a speaking warm-up. The result screen shows how many passes there were."),
  ("Can I use it for language classes?", "Yes. The prompts are yours, and it comes with Quick Review, English ESL and Spanish samples."),
 ],
 shots=[
  ("pass-the-bomb", "marketing/ptb-redesign/v2.6.1/shots/v2.6.1-bomb-running-1600x900-0.png", "Pass the Bomb in play: the prompt NAME A JOB in large letters above a cartoon bomb, with Start and Pass buttons.", "The classic bomb style. The prompt sits in a fixed box above the picture."),
  ("pass-the-bomb-jack", "marketing/ptb-redesign/v2.6.1/shots/v2.6.1-jack-running-1600x900-0.png", "The Pass the Bomb jack-in-the-box style for younger students, with the prompt NAME A JOB above a music box.", "The jack-in-the-box style for younger kids."),
  ("pass-the-bomb-bear", "marketing/ptb-redesign/v2.6.1/shots/v2.6.1-bear-running-1600x900-0.png", "The Pass the Bomb sleeping bear style, with a snoring bear under the prompt.", "Don't wake the bear!"),
  ("pass-the-bomb-baby", "marketing/ptb-redesign/v2.6.1/shots/v2.6.1-baby-running-1600x900-0.png", "The Pass the Bomb sleeping baby style, with a baby asleep in a cradle under the prompt.", "The sleeping baby style."),
 ],
 related=["five-second-battle", "forbidden-words", "sentence-slot-machine"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="five-second-battle", name="5-Second Battle", short="5-Second Battle", tag="Speaking race",
 grades="Grades 3–12", subjects="Any topic and any language, including ESL and Spanish", players="2–6 teams",
 time="10–30 minutes",
 title="5-Second Battle: Fast Speaking Review Game | Review Recess",
 description="Teams race the clock to name three things before time runs out. A fast speaking review game for 2–6 teams in any subject or language, with steals.",
 h1="5-Second Battle: a name-three-things speaking race for 2–6 teams",
 intro=[
  "5-Second Battle is a quick-fire speaking game. A team gets a prompt like \"Name 3 planets\" and has to answer out loud before the countdown hits zero. If they miss, the next team can steal.",
  "It works for any topic and any language, with English review, English ESL and Spanish samples. Play with 2–6 teams in Grades 3–12.",
 ],
 setup=[
  "Choose the number of teams (2–6) and type the team names, or load them from a roster.",
  "Set the seconds per question and the steal time (each from 3 to 30 seconds).",
  "Choose the question order (random or in order) and your question bank. Each line is a prompt and a model answer, separated by |.",
  "Press ▶ START GAME.",
 ],
 round=[
  "The prompt appears for the team whose turn it is. Questions rotate through the teams in order.",
  "Press ⚡ START TIMER. The team answers out loud before the buzzer.",
  "Press ✓ CORRECT if they did it, or 🔥 STEAL to give the next team a chance with the steal timer. Press STEAL again to pass it on until every other team has tried.",
  "Press 👀 REVEAL to show the model answer, then NEXT →.",
 ],
 scoring=[
  "A correct answer is +1 for the team that gave it, including on a steal.",
  "Each team has − / + buttons for manual changes. Scores never go below zero.",
  "Press 🏁 End game to show the winner (or a draw) and the final scores.",
 ],
 modes=[
  ("2–6 teams", "Turns rotate through the teams automatically."),
  ("Steals", "On a miss, the next team in order gets a chance, and the steal keeps passing until every team has tried."),
  ("Random or in order", "Shuffle the prompts, or play them in your order."),
 ],
 settings=[
  ("Seconds per question", "3, 5, 7, 10, 15, 20, 25 or 30 seconds."),
  ("Steal time", "3, 5, 7, 10, 15, 20, 25 or 30 seconds."),
  ("Model answers", "Add an answer after the | so you can reveal examples after each turn."),
  ("Keyboard", "Space starts the timer, R reveals, C marks correct, S steals, and → or N goes to the next question."),
 ],
 tips=[
  "Use 10–15 seconds for younger students and English learners, and 5 seconds for a real challenge.",
  "Have each team choose a different speaker every turn so everyone answers.",
  "Reveal the model answer every time. It's a quick way to teach new vocabulary.",
  "Use it as a five-minute bell-ringer or an exit activity.",
 ],
 subject_ideas={
  "ELA": "Name 3 verbs, 3 adjectives, 3 words with a silent letter.",
  "Math": "Name 3 multiples of 4, 3 shapes with right angles, 3 prime numbers.",
  "Science": "Name 3 mammals, 3 planets, 3 sources of energy.",
  "Social studies": "Name 3 U.S. states, 3 continents, 3 oceans.",
 },
 full_extra="",
 faq=[
  ("How many teams can play?", "From 2 to 6. Questions rotate through the teams automatically."),
  ("Can I give students more time?", "Yes. Choose anything from 3 to 30 seconds per question, and a separate steal time from 3 to 30 seconds."),
  ("Does it work for world languages?", "Yes. Prompts can be in any language, and it comes with English ESL and Spanish samples."),
  ("Who decides if an answer is correct?", "You do. Press ✓ CORRECT or 🔥 STEAL after each turn."),
 ],
 shots=[
  ("five-second-battle", "v2-screenshots/v2.5-fsb/game-4teams-light-steal.png", "5-Second Battle with four teams: the prompt NAME 3 CONTINENTS, a countdown and a STEAL banner.", "A steal in a four-team game."),
  ("five-second-battle-turn", "v2-screenshots/v2.5-fsb/game-6teams-light-turn.png", "5-Second Battle with six teams across the top and the prompt NAME 3 INSTRUMENTS.", "Up to six teams take turns in order."),
  ("five-second-battle-end", "v2-screenshots/v2.5-fsb/end-6teams-light.png", "5-Second Battle final scores, with Team Fox as the winner.", "Final scores at the end of the game."),
 ],
 related=["pass-the-bomb", "forbidden-words", "sentence-slot-machine"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="sentence-slot-machine", name="Sentence Slot Machine", short="Sentence Slot Machine", tag="Sentence building",
 grades="Grades 3–12", subjects="ELA, ESL and world languages", players="2 teams",
 time="10–30 minutes",
 title="Sentence Slot Machine: Sentence-Building Game | Review Recess",
 description="Spin up to five reels of words and phrases, then build a full sentence out loud before the timer runs out. A speaking game for ELA, ESL and world languages.",
 h1="Sentence Slot Machine: spin the reels and build a sentence out loud",
 intro=[
  "Sentence Slot Machine gives students a random who, what, when and where, and challenges them to say one complete sentence that uses all of it before time runs out.",
  "You choose what goes on every reel, so it fits any grammar point or vocabulary list. It's built for two teams and suits ELA, ESL and world-language classes in Grades 3–12.",
 ],
 setup=[
  "Type the two team names, or load them from a roster.",
  "Choose the speaking time (3 to 60 seconds) and whether the timer starts automatically after the spin.",
  "Fill the reels. There are up to 5 reels, each with a title and one item per line. Turn reels on or off. You need at least 2.",
  "Press ▶ START GAME.",
 ],
 round=[
  "Press 🎰 SPIN! The reels stop one by one.",
  "The team says a sentence out loud that uses every result. The timer starts after the spin, or when you press ⏱ START TIMER.",
  "Press ✓ CORRECT or ✗ MISS. Then it's the other team's turn.",
 ],
 scoring=[
  "A correct sentence is +1, or +2 if a DOUBLE POINTS item came up.",
  "A miss scores nothing.",
  "Use − / + to adjust the scores, and 🏁 End game for the final scores.",
 ],
 modes=[
  ("Up to 5 reels", "For example WHO?, WHAT?, WHEN?, WHERE? and a CHAOS reel."),
  ("Chaos items", "Items like ⚡ 3 SECONDS change that turn's timer, and 💣 DOUBLE POINTS doubles the score."),
  ("Automatic or teacher-started timer", "Start the countdown right after the spin, or give students thinking time first."),
 ],
 settings=[
  ("Speaking time", "3, 5, 7, 10, 15, 20, 30, 45 or 60 seconds."),
  ("Reel editor", "See the reels side by side with item counts, reorder them, add up to 5, or paste a column from a spreadsheet."),
  ("Samples", "English: Who? What? When? Where?, and English ESL: Daily routines."),
  ("Keyboard", "Space spins, C marks correct, X marks a miss and T starts the timer."),
 ],
 tips=[
  "Set a grammar target before you spin, such as the past tense, a compound sentence or a question.",
  "Give English learners 30–60 seconds and a sentence frame on the board.",
  "Turn on the CHAOS reel once students are confident.",
  "Ask the other team to repeat or improve the sentence for a bonus point.",
 ],
 subject_ideas={
  "ELA": "Subjects, verbs and time phrases to practice tenses and complete sentences.",
  "World languages": "Reels in Spanish or French to practice conjugation and word order.",
  "Science": "Animals, habitats and adaptations to build science sentences.",
  "Social studies": "People, actions and places from the unit to retell history.",
 },
 full_extra="",
 faq=[
  ("How many reels can I use?", "Up to 5, and at least 2. Each reel can be turned on or off."),
  ("Can I make the timer longer?", "Yes. Choose up to 60 seconds of speaking time."),
  ("Can I use it for Spanish or French?", "Yes. The reels can hold any words or phrases in any language."),
  ("How many teams can play?", "Two teams take turns."),
 ],
 shots=[
  ("sentence-slot-machine", "v2-screenshots/v2.5-ssm/timer-60-light.png", "Sentence Slot Machine with three reels reading The bus driver, sings a song and every morning, and a 60-second timer.", "Spin, then build the sentence before the timer ends."),
  ("sentence-slot-machine-reels", "v2-screenshots/v2.4/slot-reel-editor-light.png", "The Sentence Slot Machine reel editor, with the reels side by side and the items on each reel.", "Edit every reel side by side."),
  ("sentence-slot-machine-setup", "v2-screenshots/v2.4/slot-setup-english.png", "Sentence Slot Machine setup with team names, speaking time, the automatic timer and five reels.", "Setup: teams, timer and reels."),
 ],
 related=["sentence-snap", "five-second-battle", "word-magnets"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="mystery-cat", name="Mystery Cat", short="Mystery Cat", tag="Parts-of-speech puzzle",
 grades="Grades 2–9", subjects="Parts of speech, vocabulary and facts", players="2–6 teams",
 time="15–30 minutes",
 title="Mystery Cat: Parts of Speech Puzzle Game | Review Recess",
 description="Teams guess letters to reveal the hidden words in a sentence. Practice nouns, verbs, adjectives, adverbs and more, with a name-the-part-of-speech bonus.",
 h1="Mystery Cat: a parts-of-speech letter-guessing puzzle for teams",
 intro=[
  "In Mystery Cat, a sentence appears with some of its words hidden. Teams take turns guessing letters to reveal them, then try to solve the words and finally the whole sentence. A detective cat reacts to every guess.",
  "Each bank focuses on one part of speech (nouns, verbs, adjectives, adverbs, pronouns, prepositions or conjunctions) or on general vocabulary, so it's a grammar game and a vocabulary game in one. It suits Grades 2–9 with 2–6 teams.",
 ],
 setup=[
  "Choose a phrase bank. Each bank has a word type, and all the wording on screen follows it, for example \"Guess a verb\".",
  "Turn the \"Name the part of speech\" bonus on or off.",
  "Choose the number of teams (2–6) and type each team's name and members, or load the teams from a roster. Press START GAME.",
 ],
 round=[
  "The sentence appears with the hidden words as blanks. The turn display shows the team and the player.",
  "The player guesses a letter by clicking it or typing it. Every matching letter is revealed.",
  "On its turn, a team can press 💬 Guess a word (the label follows the word type). You see the answer and mark it ✓ Correct or ✗ Incorrect.",
  "When 3 or fewer hidden letters are left, the final challenge starts: guess the whole phrase.",
  "Press NEXT CAT ➜ for the next sentence.",
 ],
 scoring=[
  "A letter that's in the phrase is +1, and a letter that isn't is −1.",
  "A correct word is +2, and an incorrect word is −1.",
  "In the final challenge, the whole phrase is +5. A wrong guess is −2 and passes to the next team.",
  "With the bonus on, the team that solves a word can win +1 more for naming its part of speech.",
 ],
 modes=[
  ("Word type per bank", "Adjectives, nouns, verbs, adverbs, pronouns, prepositions, conjunctions or vocabulary."),
  ("Mixed parts of speech", "Tag words like {quickly|adverb}, so one sentence can hide several types of word."),
  ("Name the part of speech bonus", "Off by default. After a word is solved, show the answer and give +1 or no bonus. Solved words get a colored tag."),
 ],
 settings=[
  ("Phrase banks", "Hide words by putting them in {braces}. It comes with 8 sample banks for Grades 2–6: one per part of speech, plus a mixed bank."),
  ("Teams", "2–6 teams, with players who rotate within each team."),
  ("Fits on one screen", "Everything is visible without scrolling, even with 6 teams on a 1280 × 720 screen."),
 ],
 tips=[
  "Before each new sentence, ask the class which part of speech is hidden and why.",
  "Use the bonus to check understanding: students must name the part of speech, not just spell the word.",
  "Write sentences from your current class novel or unit, so grammar practice reinforces content.",
  "Use ↺ Restart cat (scores are kept) if a sentence was too hard.",
 ],
 subject_ideas={
  "ELA": "Adjectives in descriptive writing, strong verbs, adverbs of manner, conjunctions in compound sentences.",
  "Science": "Facts with hidden key terms: Plants make food through {photosynthesis}.",
  "Social studies": "Facts with hidden names and places from the unit.",
  "Math": "Math vocabulary hidden in definitions: A {triangle} has three sides.",
 },
 full_extra="",
 faq=[
  ("Is it only for adjectives?", "No. Each bank can focus on adjectives, nouns, verbs, adverbs, pronouns, prepositions, conjunctions or general vocabulary, and tags let you mix word types in one sentence."),
  ("How do I hide a word?", "Put it in braces, for example: The {fluffy} cat slept. To mark its part of speech in a mixed bank, write {quickly|adverb}."),
  ("Do students need to scroll?", "No. The play screen fits on one screen, even with 6 teams."),
  ("Can students type their letter guesses?", "Yes. Letters can be clicked on screen or typed on the keyboard."),
 ],
 shots=[
  ("mystery-cat", "marketing/mc-redesign/03-play-verb-mode.png", "Mystery Cat in play: a detective cat on the left, a sentence with partly revealed hidden words, and team scores along the bottom.", "Guess letters to reveal the hidden words."),
  ("mystery-cat-mixed", "marketing/mc-redesign/04b-mixed-mode-tags-on-board.png", "Mystery Cat in mixed mode, with solved words tagged pronoun and noun.", "Mixed mode: solved words get a part-of-speech tag."),
  ("mystery-cat-setup", "marketing/mc-redesign/02-setup.png", "Mystery Cat setup with the phrase bank, the part-of-speech bonus, how to play and the team names.", "Setup: bank, bonus and teams."),
 ],
 related=["word-magnets", "letter-lifeline", "word-scramble"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="word-magnets", name="Review Recess Word Magnets", short="Review Recess Word Magnets", tag="Drag-and-drop grammar",
 grades="Grades 3–9", subjects="ELA grammar", players="The whole class, with students called up at random",
 time="10–25 minutes",
 title="Review Recess Word Magnets: Drag-and-Drop Grammar Game",
 description="Drag the gold word onto its partner: adverbs, adjectives, subjects, objects, pronouns and prepositional phrases. A whole-class grammar game for Grades 3–9.",
 h1="Review Recess Word Magnets: a drag-and-drop grammar game for parts of speech",
 intro=[
  "Review Recess Word Magnets turns sentences into magnet tiles on a board. One word is a gold magnet, and students drag it onto the word it belongs with: the word an adverb modifies, the noun an adjective describes, a pronoun's antecedent and more. A right answer snaps on with a gold link.",
  "It's a whole-class grammar game for Grades 3–9 that works with a mouse or by touch on an interactive board. It was formerly called \"What Does It Modify?\".",
 ],
 setup=[
  "Choose a mode: one of six grammar modes, or Mixed, where each sentence keeps its own mode. Each mode card shows how many sentences the bank has for it.",
  "Choose a sentence bank, and use ☑ Choose… to pick which sentences to use.",
  "If you like, type your class list (or load a roster) so the game can call students up.",
  "Press ▶ Start game.",
 ],
 round=[
  "A sentence appears as word tiles, with one gold magnet tile. The instruction line tells students what to find.",
  "Press 🎲 Call a student. Everyone is called once before anyone repeats.",
  "The student drags the gold magnet onto its partner word, or taps the partner word.",
  "If it's right, the magnet snaps on with a gold link and a ✓, and the feedback bar explains why. If it's wrong, the tile shakes and gets a red ✕, and the student can try again.",
  "Press Next sentence ▸. Use 👀 Reveal to show the answer, or Skip ▸ to move on.",
 ],
 scoring=[
  "The class earns a point for each sentence solved and builds a streak for answers in a row.",
  "Streak badges appear at 3, 5, 7 and 10, with confetti every 5 in a row. A wrong answer resets the streak.",
  "Game over shows the class score, the best streak and the accuracy.",
 ],
 modes=[
  ("Adverbs", "Drag the adverb onto the verb, adjective or adverb it modifies (\"What does it modify?\")."),
  ("Adjectives", "Drag the adjective onto the noun it describes."),
  ("Subjects and objects", "Drag the verb onto its subject, or onto its direct object."),
  ("Pronouns", "Drag the pronoun onto its antecedent."),
  ("Prepositional phrases", "The whole phrase is one magnet. Drag it onto the word it modifies."),
  ("Mixed", "Each sentence keeps its own mode, for cumulative review."),
 ],
 settings=[
  ("Sentence banks", "Each row has a sentence, the magnet word, the partner word and the mode. Samples for Grades 3–8 cover all six modes, plus a mixed review and a 40-sentence adverb bank."),
  ("Touch and keyboard", "Drag with a mouse, pen or finger, tap the partner word, or use Tab and Enter."),
  ("Fixed sentence area", "One font size for the whole bank, so nothing jumps between short and long sentences."),
 ],
 tips=[
  "Ask the student to explain their choice out loud before they drag. The feedback bar then confirms it.",
  "Start a unit with one mode, then switch to Mixed for review.",
  "Have the class show thumbs up or down before the student drops the magnet.",
  "Use the pronoun mode during writing lessons to talk about unclear antecedents.",
 ],
 subject_ideas={
  "ELA": "Adverbs, adjectives, subject-verb pairs, direct objects, pronoun antecedents and prepositional phrases.",
  "Science": "Write sentences from your science unit, so grammar practice reviews content too.",
  "Social studies": "Use sentences about historical events to practice subjects and objects.",
  "ESL": "Adjective-noun and pronoun practice with visual, hands-on feedback.",
 },
 full_extra="",
 faq=[
  ("Is this the old \"What Does It Modify?\" game?", "Yes. It was renamed Review Recess Word Magnets and now has six grammar modes plus Mixed. The adverb mode still asks \"What does it modify?\"."),
  ("Does it work on an interactive whiteboard?", "Yes. Students can drag with a finger or a pen, or simply tap the partner word."),
  ("Are student names saved?", "No. Names you type stay on the screen only and are never saved."),
  ("Which grammar skills does it cover?", "Adverbs, adjectives, subjects, direct objects, pronouns and their antecedents, and prepositional phrases."),
 ],
 shots=[
  ("word-magnets", "marketing/wdim-redesign/02-mode-adverb.png", "Review Recess Word Magnets: the sentence The singer performed exceptionally well as word tiles, with the gold adverb exceptionally ready to drag onto the word it modifies.", "Adverb mode: drag the gold adverb onto the word it modifies."),
  ("word-magnets-drag", "marketing/wdim-redesign/08-mid-drag.png", "A student dragging the gold adjective fluffy across the magnet board toward the noun it describes.", "Drag with a mouse or by touch."),
  ("word-magnets-correct", "marketing/wdim-redesign/09-correct-snap.png", "A correct answer in Review Recess Word Magnets: fluffy snapped onto dog with a gold link and the feedback fluffy describes dog.", "A right answer snaps on with a gold link."),
  ("word-magnets-pronoun", "marketing/wdim-redesign/06-mode-pronoun.png", "Review Recess Word Magnets pronoun mode: drag the gold pronoun she onto its antecedent.", "Pronoun mode: find the antecedent."),
 ],
 related=["mystery-cat", "sentence-snap", "sentence-slot-machine"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="sentence-snap", name="Review Recess Sentence Snap", short="Review Recess Sentence Snap", tag="Unscramble sentences",
 grades="Grades 2–8", subjects="ELA grammar, sentence structure and content sentences", players="The whole class, or 2–6 teams",
 time="10–25 minutes",
 title="Review Recess Sentence Snap: Unscramble-the-Sentence Game",
 description="Students drag scrambled word tiles into order to build the sentence, and correct tiles lock in green. Whole-class or 2–6 team play for Grades 2–8.",
 h1="Review Recess Sentence Snap: a drag-to-unscramble sentence game for your classroom screen",
 intro=[
  "Review Recess Sentence Snap shows a sentence as scrambled word tiles. Students drag (or tap) the tiles into order and press Check. Tiles in the right place lock in green, and wrong ones get a red ✕ so students can fix them.",
  "It's built for sentence structure, capitalization and punctuation in Grades 2–8. Play as a whole class or with 2–6 teams.",
 ],
 setup=[
  "Choose a sentence bank, and use ☑ Choose… to pick the sentences.",
  "Choose the game mode: Whole class or Teams (2–6 teams, or load a class roster).",
  "Set the sentences per game (5, 10, 15, 20 or all), the timer (off, 30 s, 60 s, 90 s or 2 min), and whether to show hints, the category and the hint button.",
  "Choose how the end mark works (locked at the end, or a tile along with any commas) and whether the first word's capital is shown or hidden. Press ▶ Start game.",
 ],
 round=[
  "The sentence appears as shuffled word tiles above a row of empty slots.",
  "Students drag each tile into a slot, or tap a tile and then a slot. Tapping a tile twice drops it into the next empty slot.",
  "Press ✓ Check. Correct tiles lock in green, and wrong ones get a red ✕. Fix them and check again.",
  "Stuck? Use 💡 Hint to show the first wrong tile, or 🔀 Shuffle again. Then press Next ▶.",
 ],
 scoring=[
  "In Teams mode, a first-try solve is 2 points, and a solve after a retry or a hint is 1 point. Use − / + to adjust.",
  "In Whole class mode, the class counts how many sentences it solves.",
  "👁 Reveal shows the answer with no points. 🏁 End game shows the podium.",
 ],
 modes=[
  ("Whole class or teams", "Solve together, or let 2–6 teams take turns."),
  ("End mark and commas", "Keep the end mark locked in place, or make it (and any commas) tiles too."),
  ("Capital letter clue", "Show the first word's capital as an easier clue, or hide it for a harder game."),
 ],
 settings=[
  ("Timer", "Off, 30 seconds, 60 seconds, 90 seconds or 2 minutes."),
  ("Hints and categories", "Show or hide each sentence's hint and category, and turn the 💡 Hint button on or off."),
  ("Other correct orders", "A sentence can accept more than one correct word order."),
  ("Same-size tiles", "Tiles stay the same size all game, in the light, dark and high-contrast themes."),
 ],
 tips=[
  "Hide the capital letter and make the end mark a tile once students are ready for a challenge.",
  "Ask students to read the finished sentence aloud with expression.",
  "Use sentences with prepositional phrases to show how word order changes meaning.",
  "In Teams mode, give each team member a turn at the board.",
 ],
 subject_ideas={
  "ELA": "Simple, compound and complex sentences, questions, and sentences with commas.",
  "Science": "Key facts from the unit, such as Plants use sunlight to make their own food.",
  "Social studies": "Sentences about events and people from the unit.",
  "ESL": "Word order in questions, adjectives and time phrases.",
 },
 full_extra="",
 faq=[
  ("Can students play on an interactive whiteboard?", "Yes. Drag the tiles with a finger, or tap a tile and then a slot."),
  ("What if a sentence has more than one correct order?", "You can add other correct orders to a sentence, and any of them is accepted."),
  ("Can I make it harder?", "Yes. Hide the first word's capital, make the end mark and commas into tiles, turn hints off, or add a timer."),
  ("How does team scoring work?", "Two points for a first-try solve, and one point after a retry or a hint."),
 ],
 shots=[
  ("sentence-snap", "marketing/new-scramble-games/sentence-snap-2-mid-drag.png", "Review Recess Sentence Snap in play: the sentence What game did the children play? partly built from word tiles, with team scores on the right.", "Drag the word tiles into order."),
  ("sentence-snap-correct", "marketing/new-scramble-games/sentence-snap-3-correct.png", "A solved sentence in Review Recess Sentence Snap, with every tile locked in green.", "Correct tiles lock in green."),
  ("sentence-snap-setup", "marketing/new-scramble-games/sentence-snap-1-setup.png", "Review Recess Sentence Snap setup with the sentence bank, whole class or teams, and the timer, hint, end mark and capital letter options.", "Setup: mode, timer, hints and punctuation options."),
  ("sentence-snap-win", "marketing/new-scramble-games/sentence-snap-5-win.png", "The Review Recess Sentence Snap end-of-game podium with the winning team.", "The podium at the end of the game."),
 ],
 related=["word-scramble", "word-magnets", "sentence-slot-machine"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="word-scramble", name="Word Scramble", short="Word Scramble", tag="Unscramble words",
 grades="Grades 2–8", subjects="Spelling and vocabulary in any subject", players="The whole class, or 2–6 teams",
 time="10–25 minutes",
 title="Word Scramble: Unscramble Vocabulary Game | Review Recess",
 description="Students drag scrambled letter tiles to spell the word, with an optional clue. A spelling and vocabulary game for the whole class or 2–6 teams in Grades 2–8.",
 h1="Word Scramble: a drag-the-letters unscramble game for spelling and vocabulary",
 intro=[
  "Word Scramble shows a word as mixed-up letter tiles, with an optional clue or definition. Students drag the letters into order and press Check. Letters in the right place lock in green.",
  "Use it for spelling lists and content vocabulary in Grades 2–8. Play as a whole class or with 2–6 teams, with an optional timer.",
 ],
 setup=[
  "Choose a word bank, and use ☑ Choose… to pick the words.",
  "Choose the game mode: Whole class or Teams (2–6 teams, or load a class roster).",
  "Set the words per game (5, 10, 15, 20 or all), the timer, clues, the category, the hint button, and lowercase or UPPERCASE letters.",
  "Press ▶ Start game.",
 ],
 round=[
  "The clue appears, with the scrambled letter tiles below it.",
  "Students drag each letter into a slot, or tap a letter and then a slot.",
  "Press ✓ Check. Letters in the right place lock in green, and wrong ones get a red ✕.",
  "Stuck? 🔀 Shuffle again mixes the remaining letters, and 💡 Hint shows the first wrong letter. Then press Next ▶.",
 ],
 scoring=[
  "In Teams mode, a first-try solve is 2 points, and a solve after a retry or a hint is 1 point. Use − / + to adjust.",
  "In Whole class mode, the class counts how many words it solves.",
  "👁 Reveal shows the word with no points. 🏁 End game shows the podium.",
 ],
 modes=[
  ("Whole class or teams", "Solve together, or let 2–6 teams take turns."),
  ("Clues on or off", "Show the definition as a clue, or hide it for a pure spelling challenge."),
  ("Other accepted answers", "A word can accept other correct answers, such as listen and silent."),
 ],
 settings=[
  ("Timer", "Off, 30 seconds, 60 seconds, 90 seconds or 2 minutes."),
  ("Letters", "Lowercase or UPPERCASE tiles."),
  ("Categories", "Show each word's category, such as Life science, as an extra clue."),
  ("Same-size tiles", "Tiles stay the same size all game, in the light, dark and high-contrast themes."),
 ],
 tips=[
  "Write clues as definitions, so students practice meaning as well as spelling.",
  "Use UPPERCASE tiles for younger students who are still learning lowercase letters.",
  "Ask students to use the word in a sentence after they solve it.",
  "Turn clues off for a second round with the same list.",
 ],
 subject_ideas={
  "Science": "Habitat, photosynthesis, condensation, with definitions as clues.",
  "ELA": "Weekly spelling lists, vocabulary from a novel, homophones.",
  "Math": "Denominator, perimeter, equation, symmetry.",
  "Social studies": "Places, people and terms from the unit.",
 },
 full_extra="",
 faq=[
  ("Can I add clues or definitions?", "Yes. Each word can have a clue or definition, and you can show or hide clues on the setup screen."),
  ("What if the letters make another word too?", "You can add other accepted answers, so an anagram like silent for listen still counts."),
  ("Does it work on an interactive whiteboard?", "Yes. Drag the letters with a finger, or tap a letter and then a slot."),
  ("Can I play without teams?", "Yes. Whole class mode lets everyone solve together and counts how many words you get."),
 ],
 shots=[
  ("word-scramble", "marketing/new-scramble-games/word-scramble-2-mid-drag.png", "Word Scramble in play: the clue How plants use sunlight to make their own food, with scrambled letter tiles being dragged into slots.", "Drag the letters into order to spell the word."),
  ("word-scramble-correct", "marketing/new-scramble-games/word-scramble-3-correct.png", "A solved word in Word Scramble: photosynthesis, with every letter locked in green.", "Correct letters lock in green."),
  ("word-scramble-setup", "marketing/new-scramble-games/word-scramble-1-setup.png", "Word Scramble setup with the word bank, whole class or teams, and the timer, clue and letter case options.", "Setup: mode, timer, clues and letter case."),
  ("word-scramble-teams", "marketing/new-scramble-games/word-scramble-4-team-scoreboard.png", "Word Scramble with team scores on the right and red marks on the letters in the wrong place.", "Wrong letters get a red mark, so students can fix them."),
 ],
 related=["letter-lifeline", "sentence-snap", "mystery-cat"],
))

# =============================================================================================
GAME_PAGES.append(dict(
 slug="tic-tac-toe-quiz-game", name="Tic-Tac-Toe Quiz Game", short="Tic-Tac-Toe Quiz Game", tag="Team quiz",
 grades="Grades 2–12", subjects="Any subject", players="2 teams: X vs O",
 time="10–30 minutes",
 title="Tic-Tac-Toe Quiz Game for Two Teams | Review Recess",
 description="Two teams answer review questions to claim squares on a tic-tac-toe board, and three in a row wins the round. Steal mode and player rotation for any subject.",
 h1="Tic-Tac-Toe Quiz Game: answer a question to claim a square",
 intro=[
  "The Tic-Tac-Toe Quiz Game puts a review question behind every square. Two teams, X and O, take turns choosing a square and answering. A correct answer claims it, and three in a row wins the round.",
  "Players answer in order, so every student gets a turn, not just the fastest hands. It works for any subject in Grades 2–12.",
 ],
 setup=[
  "Type the names of Team X and Team O, and list each team's players, one per line. Players rotate in order.",
  "Load a saved question bank, or type the questions as question | answer, one per line, and save the bank.",
  "Choose the game mode: Standard (a wrong answer ends the turn) or Steal Mode (the other team gets one chance).",
  "Press START GAME.",
 ],
 round=[
  "The team whose turn it is picks a square, and a question appears.",
  "The player whose turn it is answers. Press REVEAL ANSWER.",
  "Press ✓ CORRECT to claim the square, or ✕ INCORRECT. In Steal Mode, the other team's next player then gets one chance at the same question.",
  "Play passes to the other team. Keep going until a team gets three in a row or the board is full.",
 ],
 scoring=[
  "Three in a row wins the round, with confetti and a win sound. A full board with no winner is a draw.",
  "Each team has a rounds-won counter. Press NEXT ROUND to play again.",
  "A new round keeps the remaining questions and the player rotation.",
 ],
 modes=[
  ("Standard", "A wrong answer ends the turn."),
  ("Steal Mode", "After a wrong answer, the other team's next player gets one chance to steal the square."),
 ],
 settings=[
  ("Teacher panel", "↶ Undo last move, ⏭ Skip question, ↺ New round, sound on or off, full screen and 🏁 End game."),
  ("Question banks", "Save as many banks as you like, load them next lesson, or open the question sheet to edit them all at once."),
  ("No repeats", "Questions are shuffled, and none repeats until every question has been used."),
 ],
 tips=[
  "Use Steal Mode to keep the other team listening on every question.",
  "Let the team talk it over for 10 seconds, but only the player whose turn it is may answer.",
  "Play best of three or best of five rounds.",
  "Talk about strategy with older classes: the center square and corners matter.",
 ],
 subject_ideas={
  "Social studies": "Ancient civilizations, U.S. history, civics and geography.",
  "ELA": "Grammar, parallel structure, vocabulary and reading skills.",
  "Math": "Quick computation, fractions and word problems.",
  "Science": "Vocabulary, processes and true-or-false questions.",
 },
 full_extra="",
 faq=[
  ("How many students can play?", "Any number, split into two teams. List each team's players, and they answer in rotation."),
  ("What is Steal Mode?", "When a team answers incorrectly, the other team's next player gets one chance at the same question."),
  ("Can I fix a mistake?", "Yes. ↶ Undo last move is in the teacher panel."),
  ("Do questions carry over between rounds?", "Yes. A new round keeps the remaining questions and the player rotation."),
 ],
 shots=[
  ("tic-tac-toe-quiz-game", "v2-screenshots/tictactoe-light-lobby.png", "The Tic-Tac-Toe Quiz Game board, with Team X and Team O player lists on each side and a message saying it is Amy's turn.", "Players take turns in order."),
  ("tic-tac-toe-quiz-game-question", "v2-screenshots/tictactoe-light-play.png", "A Tic-Tac-Toe Quiz Game question asking what Indus cities built under their streets to carry waste away, with a Reveal Answer button.", "Every square hides a question."),
  ("tic-tac-toe-quiz-game-setup", "v2-screenshots/tictactoe-light-setup.png", "Tic-Tac-Toe Quiz Game setup with Team X and Team O names, player lists and saved question banks.", "Setup: teams, players and question bank."),
 ],
 related=["brain-board-blitz", "answer-armada", "million-point-climb"],
))

# Old URLs and #anchors that must keep working (used by build.py, _redirects and .htaccess).
OLD_SLUGS = {
    "word-magnets": ["what-does-it-modify"],
    "tic-tac-toe-quiz-game": ["quiz-tac-toe"],
    "answer-armada": ["grammar-battleships"],
}

# =============================================================================================
# PRODUCT LINES: the "Choose your version" tiers on a game page (first line: Answer Armada, Oct 2026).
# ALL WORDING BELOW IS PLACEHOLDER COPY. Phil rewrites it before launch (TpT/brand rule: no AI-written listing copy).
# Buttons come from assets/js/config.js (key = link, fallback = used when key is blank). Blank = grey "Coming soon".
# "included" lists must match what is really in each TpT download.
PRODUCT_LINES = {
 "answer-armada": dict(
  eyebrow="Choose your version",
  heading="Three ways to play Review Recess Answer Armada",
  lead="Start with the free test version on your own classroom screen, then pick the version that fits how you teach.",
  tiers=[
   dict(id="free", label="Free", name="Free test version",
        blurb="Check that Answer Armada runs on your classroom screen and school network before you buy.",
        included=["The complete game with one built-in sample set of 3rd grade multiplication facts",
                  "Opens straight from a link, with no Google sign-in",
                  "Every picture style and difficulty level",
                  "A one-page quick start guide"],
        note="The sample set can't be edited.",
        button=("FREE_VERSION_URLS.answer-armada", "", "Get the free version on TpT"),
        extra_button=("ANSWER_ARMADA.FREE_PLAY_URL", "Play the free version now")),
   dict(id="pack", label="Topic pack", name="3rd Grade Multiplication & Division Facts",
        blurb="A ready-to-play pack: open the link, pick a fact set and play. No typing questions in.",
        included=["Ready-to-play game link with 150+ multiplication and division facts in 8 sets you can mix and match",
                  "Printable question list with a teacher answer key",
                  "Teacher kit: quick start, full instructions, troubleshooting and a setup video",
                  "Student practice page and exit ticket that match the facts",
                  "Printable team cards and scoreboard"],
        note="The questions are fixed. To use your own, choose the editable version.",
        button=("ANSWER_ARMADA.PACK_TPT_URL", "", "Get the topic pack on TpT")),
   dict(id="editable", label="Most flexible", name="Editable full version",
        blurb="Use Answer Armada all year with your own questions, saved in your own Google Drive.",
        included=["Add, paste and edit as many question banks as you like, saved in a Google Sheet in your own Drive",
                  "Access to the Review Recess question bank, ready to paste in, with new questions added over time",
                  "Saved class rosters and a fair student picker",
                  "Every picture style and difficulty level",
                  "The full teacher kit and setup video"],
        note="Runs in your own Google account. A personal Gmail account works if your school blocks the game.",
        button=("ANSWER_ARMADA.EDITABLE_TPT_URL", "", "Get the editable version on TpT")),
  ],
  # comparison table: (row label, free, pack, editable). "yes" / "no" render as icons with screen-reader text.
  compare=[
   ("Plays on your smart TV or projector", "yes", "yes", "yes"),
   ("Questions", "One built-in sample set", "3rd grade multiplication & division facts (8 sets)", "Your own questions plus the question bank"),
   ("Pick which questions to use", "yes", "yes", "yes"),
   ("Add or edit your own questions", "no", "no", "yes"),
   ("Printable question list and answer key", "no", "yes", "yes"),
   ("Teacher kit and setup video", "Quick start only", "yes", "yes"),
   ("Growing question bank", "no", "no", "yes"),
   ("Saved class rosters and student picker", "no", "no", "yes"),
   ("Google sign-in", "Not needed", "Not needed", "Your own account"),
  ],
  footnote="Every version is sold or given away through our Teachers Pay Teachers store.",
 ),
}
