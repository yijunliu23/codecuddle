import React, { useState } from 'react';

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const hours = Array.from({ length: 24 }, (_, index) => index);

const App = () => {
  const [schedule, setSchedule] = useState({});
import moment from 'moment';
  const [currentUser, setCurrentUser] = useState('');
  const [commonTimesMessage, setCommonTimesMessage] = useState('');

const toggleAvailability = (day, hour) => {
    if (!currentUser.trim()) return;

    const utcHour = moment.utc().day(day).hour(hour).format();

    setSchedule((prevSchedule) => {
      const isUserPresent = hourSchedule.some(user => user === currentUser);

      const newHourSchedule = isUserPresent
        ? hourSchedule.filter(user => user !== currentUser)
        : [...hourSchedule, currentUser];

      return {
        ...prevSchedule,
        [day]: { ...daySchedule, [hour]: newHourSchedule },
      };
    });
  };

  const handleChangeUser = (event) => {
    setCurrentUser(event.target.value);
  };

  const findCommonTimes = () => {
    let allUserCounts = {};

    Object.values(schedule).forEach(day => {
      Object.values(day).forEach(hour => {
        hour.forEach(user => {
          allUserCounts[user] = (allUserCounts[user] || 0) + 1;
        });
      });
    });

    let commonTimes = [];
    let allUsers = Object.keys(allUserCounts);

    for (let day of days) {
      for (let hour of hours) {
        let hourSchedule = schedule[day]?.[hour];
        if (hourSchedule && allUsers.every(user => hourSchedule.includes(user))) {
          commonTimes.push(`${day} at ${hour}:00`);
        }
      }
    }

    if (commonTimes.length === 0) {
      setCommonTimesMessage('No common times available for all users.');
    } else {
      setCommonTimesMessage(`Common times for all users: ${commonTimes.join(', ')}.`);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter your name"
        value={currentUser}
        onChange={handleChangeUser}
      />
      <button onClick={findCommonTimes}>Find Common Available Times</button>
      <div>{commonTimesMessage}</div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid black' }}>Time/Day</th>
            {days.map((day) => (
              <th key={day} style={{ border: '1px solid black' }}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {hours.map((hour) => (
            <tr key={hour}>
              <td style={{ border: '1px solid black' }}>{hour}:00</td>
              {days.map((day) => (
                <td
                  key={day}
                  style={{
                    border: '1px solid black',
                    background: schedule[day]?.[hour]?.includes(currentUser) ? 'lightgreen' : 'none',
                    cursor: 'pointer',
                  }}
                  onClick={() => toggleAvailability(day, hour)}
                >
                  {schedule[day]?.[hour]?.join(', ') || ''}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
