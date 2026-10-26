/* ===================================================================
   REVIEW RECESS — SITE LINKS.  THIS IS THE ONLY FILE YOU NEED TO EDIT.
   -------------------------------------------------------------------
   Paste each link between the quotes, save, and re-upload the site.
   Leave a value as "" and every button that uses it shows
   "Coming soon" instead of a broken link.

   Rules (anything else is ignored and treated as blank):
     * URLs must start with https://
     * CONTACT_EMAIL is just the address, e.g. "support@reviewrecess.com"
   =================================================================== */
window.RR_CONFIG = {
  // Your TpT store page, e.g. "https://www.teacherspayteachers.com/store/review-recess"
  TPT_STORE_URL: "https://www.teacherspayteachers.com/store/review-recess",

  // Your installation-help chatbot page (help only, no selling)
  SUPPORT_CHATBOT_URL: "",      // PLACEHOLDER

  // Support email address shown on Help, About, Privacy and Terms
  CONTACT_EMAIL: "support@reviewrecess.com",

  // Optional: each game's own TpT page. Blank = the game page's "Get it on TpT" button uses TPT_STORE_URL above.
  TPT_GAME_URLS: {
    "answer-armada": "",
    "brain-board-blitz": "",
    "million-point-climb": "",
    "forbidden-words": "",
    "letter-lifeline": "",
    "pass-the-bomb": "",
    "five-second-battle": "",
    "sentence-slot-machine": "",
    "mystery-cat": "",
    "word-magnets": "",
    "sentence-snap": "",
    "word-scramble": "",
    "tic-tac-toe-quiz-game": ""
  },

  // Optional: each game's FREE version link (TpT freebie page). Blank = the "Try the free version" button is hidden.
  FREE_VERSION_URLS: {
    "answer-armada": "",
    "brain-board-blitz": "",
    "million-point-climb": "",
    "forbidden-words": "",
    "letter-lifeline": "",
    "pass-the-bomb": "",
    "five-second-battle": "",
    "sentence-slot-machine": "",
    "mystery-cat": "",
    "word-magnets": "",
    "sentence-snap": "",
    "word-scramble": "",
    "tic-tac-toe-quiz-game": ""
  },

  // FIRST PRODUCT LINE: Review Recess Answer Armada (the "Choose your version" section on /games/answer-armada/
  // and the Answer Armada block on the Home page). TpT product pages only. Blank = grey "Coming soon" button.
  //   Free test version button  -> FREE_VERSION_URLS["answer-armada"] above (the TpT freebie page)
  ANSWER_ARMADA: {
    PACK_TPT_URL: "",       // TpT page: Answer Armada, 3rd Grade Multiplication & Division Facts (non-editable topic pack)
    EDITABLE_TPT_URL: "",   // TpT page: Answer Armada editable full version + growing question bank
    // Optional extra "Play the free version now" button that opens the free game directly (not through TpT).
    // Left blank on purpose: the site sends teachers to TpT for every version. The button stays hidden while blank.
    FREE_PLAY_URL: ""
  },

  // Your YouTube channel (preview and how-to videos)
  YOUTUBE_URL: ""               // PLACEHOLDER
};
