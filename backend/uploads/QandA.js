import React, { useState } from 'react';

const App = () => {
  const [question, setQuestion] = useState('');
  const [questions, setQuestions] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      const newQuestion = {
        id: Date.now(),
        text: question,
        votes: 0,
        answers: [], // Initialize answers as an empty array
      };
      setQuestions([...questions, newQuestion]);
      setQuestion('');
    }
  };

  const handleUpvote = (id) => {
    setQuestions(
      questions.map((q) => (q.id === id ? { ...q, votes: q.votes + 1 } : q))
    );
  };

  const handleAnswer = (id, answer) => {
    setQuestions(
      questions.map((q) =>
        q.id === id ? { ...q, answers: [...q.answers, answer] } : q
      )
    );
  };

  return (
    <div>
      <h1>Simple Q&A</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question"
        />
        <button type="submit">Submit</button>
      </form>
      <ul>
        {questions
          .sort((a, b) => b.votes - a.votes)
          .map((q) => (
            <li key={q.id}>
              <strong>{q.text}</strong> - Votes: {q.votes}
              <button onClick={() => handleUpvote(q.id)}>Upvote</button>
              <div>
                <input
                  type="text"
                  placeholder="Enter an answer"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      handleAnswer(q.id, e.target.value);
                      e.target.value = '';
                    }
                  }}
                />
              </div>
              {q.answers && q.answers.length > 0 && (
                <ul>
                  {q.answers.map((answer, index) => (
                    <li key={index}>{answer}</li>
                  ))}
                </ul>
              )}
            </li>
          ))}
      </ul>
    </div>
  );
};

export default App;