/** Fake inventory with the real edition identities and no live deployment ids. */

export function seededRandomInt(seed) {
  let state = seed >>> 0;
  return (max) => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state % max;
  };
}

export function fakeDestination(id) {
  return `https://script.google.com/macros/s/${id}/exec`;
}

const ROWS = [
  ['word-magnets', 'full', 'adverb-game', 'What Does It Modify?'],
  ['answer-armada', 'editable', 'battleships', 'Review Recess Answer Armada'],
  ['five-second-battle', 'full', 'five-second-battle', '5-Second Battle'],
  ['letter-lifeline', 'full', 'hangman', 'Letter Lifeline'],
  ['brain-board-blitz', 'full', 'jeopardy', 'Brain Board Blitz'],
  ['million-point-climb', 'full', 'millionaire', 'Million Point Climb'],
  ['mystery-cat', 'full', 'mystery-cat', 'Mystery Cat'],
  ['pass-the-bomb', 'full', 'pass-the-bomb', 'Pass the Bomb'],
  ['sentence-slot-machine', 'full', 'slot-machine', 'Sentence Slot Machine'],
  ['forbidden-words', 'full', 'taboo', 'Forbidden Words'],
  ['tic-tac-toe-quiz-game', 'full', 'tictactoe', 'Tic-Tac-Toe Quiz Game'],
  ['sentence-snap', 'full', 'sentence-snap', 'Sentence Snap'],
  ['word-scramble', 'full', 'word-scramble', 'Word Scramble'],
  ['sentence-snap', 'free', 'sentence-snap-free', 'Sentence Snap (Free)'],
  ['word-scramble', 'free', 'word-scramble-free', 'Word Scramble (Free)'],
  ['letter-lifeline', 'free', 'hangman-free', 'Letter Lifeline (Free)'],
  ['five-second-battle', 'free', 'five-second-battle-free', '5-Second Battle (Free)'],
  ['sentence-slot-machine', 'free', 'slot-machine-free', 'Sentence Slot Machine (Free)'],
  ['mystery-cat', 'free', 'mystery-cat-free', 'Review Recess Mystery Cat (Free)'],
  ['word-magnets', 'free', 'adverb-game-free', 'Review Recess Word Magnets (Free)'],
  ['million-point-climb', 'free', 'millionaire-free', 'Review Recess Million Point Climb (Free)'],
  ['answer-armada', 'free', 'battleships-free', 'Review Recess Answer Armada (Free)'],
  ['pass-the-bomb', 'free', 'pass-the-bomb-free', 'Review Recess Pass the Bomb (Free)'],
  ['forbidden-words', 'free', 'taboo-free', 'Review Recess Forbidden Words (Free)'],
  ['brain-board-blitz', 'free', 'jeopardy-free', 'Review Recess Brain Board Blitz (Free)'],
  ['tic-tac-toe-quiz-game', 'free', 'tictactoe-free', 'Review Recess Tic-Tac-Toe Quiz Game (Free)'],
  ['answer-armada', 'grade-3-multiplication-division-facts', 'battleships-pack', 'Review Recess Answer Armada – 3rd Grade Multiplication & Division Facts (Pack)'],
  ['telling-time', 'full', 'telling-time', 'Review Recess What’s the Time, Mr. Wolf?'],
  ['word-morph', 'full', 'word-morph', 'Review Recess Word Morph'],
];

export const INVENTORY = {
  editions: ROWS.map(([game_slug, edition, source_game_key, display_name], index) => {
    const deployment_id = `FAKEdep${String(index + 1).padStart(4, '0')}notlive`;
    return {
      game_slug,
      edition,
      source_game_key,
      display_name,
      current_deployment_url: fakeDestination(deployment_id),
      deployment_id,
      source_version: '',
      notes: '',
    };
  }),
};
