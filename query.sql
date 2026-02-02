CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE
);

INSERT INTO users (password)
VALUES ('AwesomePassword123')



ALTER TABLE user_workouts ADD COLUMN affected_muscle TEXT ;

UPDATE users 
SET id = '3' 
WHERE name = 'Jane';

SELECT * FROM users;

CREATE TABLE user_workouts (
  user_id INTEGER,
  workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
  workout_name TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE user_workouts_prs (
  workout_id INTEGER,
  workout_weight INTEGER,
  workout_reps INTEGER,
  duration_minutes INTEGER,
  FOREIGN KEY (workout_id) REFERENCES user_workouts(workout_id)
);

DELETE FROM users WHERE id = 3;

ALTER TABLE user_workouts DROP COLUMN workout_id;

DROP TABLE user_workouts;


SELECT
    user_workouts.workout_name,
    user_workouts.affected_muscle,
    user_workouts_prs.workout_weight,
    user_workouts_prs.workout_reps,
    user_workouts_prs.duration_minutes
FROM user_workouts
JOIN user_workouts_prs ON user_workouts.user_id = user_workouts_prs.workout_id
WHERE user_workouts.user_id = 5;