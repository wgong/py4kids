-- Assuming TABLE_H7_TASK is 'habits7_task'
-- Assuming the current date is '2024-10-16' for created_at and updated_at
-- Assuming 'h7user1@gmail.com' as the user for created_by and updated_by

INSERT INTO habits7_task (task_name, description, task_group, is_urgent, is_important, status, pct_completed, due_date, task_type, note, created_by, created_at, updated_by, updated_at)
VALUES 
('Submit conference paper on deep learning', 'Finalize and submit the paper on recent deep learning advancements', 'Work', 'Y', 'Y', 'Doing', '75%', '2024-11-01', 'research', 'Remember to include latest experimental results', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Prepare for AI ethics seminar presentation', 'Create slides and talking points for the upcoming ethics in AI seminar', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-11-15', 'learning', 'Focus on recent controversies in AI applications', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Debug neural network model', 'Identify and fix issues in the current neural network implementation', 'Work', 'Y', 'Y', 'Doing', '50%', '2024-10-20', 'project', 'Check for overfitting in the validation set', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Grocery shopping', 'Buy essentials for the week', 'Personal', 'Y', 'N', 'ToDo', '0%', '2024-10-18', '', 'Remember to buy vegetables and fruits', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Review latest papers on reinforcement learning', 'Read and summarize recent advancements in RL', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-10-30', 'learning', 'Focus on papers from top conferences like NeurIPS and ICML', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Schedule dentist appointment', 'Book a check-up with Dr. Smith', 'Personal', 'N', 'N', 'ToDo', '0%', '2024-11-30', '', 'Ask about wisdom tooth extraction', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Meet with thesis advisor', 'Discuss progress and next steps for PhD thesis', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-19', 'research', 'Prepare summary of recent experiments', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Prepare dataset for machine learning experiment', 'Clean and preprocess data for the next ML model', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-10-25', 'project', 'Ensure proper normalization and feature scaling', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Plan weekend hike', 'Organize a hike with friends for the coming weekend', 'Personal', 'N', 'N', 'ToDo', '0%', '2024-10-21', 'fun', 'Check weather forecast and trail conditions', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Submit progress report to department', 'Compile and submit monthly PhD progress report', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-31', 'project', 'Include summary of recent paper submissions and experiment results', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Attend friend''s birthday party', 'Celebrate with friends at John''s birthday party', 'Personal', 'Y', 'N', 'ToDo', '0%', '2024-10-22', 'fun', 'Don''t forget to bring a gift', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Optimize code for GPU acceleration', 'Refactor current codebase to utilize GPU more efficiently', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-11-10', 'project', 'Focus on the most computationally intensive parts first', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Pay rent', 'Transfer monthly rent to landlord', 'Personal', 'Y', 'Y', 'ToDo', '0%', '2024-10-31', '', 'Set up automatic payment for future months', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Write blog post on recent AI breakthroughs', 'Summarize and explain recent advancements in AI for the lab blog', 'Work', 'N', 'N', 'ToDo', '0%', '2024-11-15', 'research', 'Include insights from the latest conference', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Exercise at gym', 'Complete weekly workout routine', 'Personal', 'N', 'Y', 'ToDo', '0%', '2024-10-20', '', 'Focus on cardio and upper body this week', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Prepare for teaching assistant duties', 'Review material and prepare for upcoming TA session', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-18', 'learning', 'Create practice problems for students', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Call parents', 'Weekly check-in call with family', 'Personal', 'N', 'Y', 'ToDo', '0%', '2024-10-20', '', 'Update them on recent research progress', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Attend research group meeting', 'Participate in weekly lab meeting and present recent findings', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-17', 'research', 'Prepare slides on the latest experiment results', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Update CV', 'Add recent publications and projects to curriculum vitae', 'Personal', 'N', 'N', 'ToDo', '0%', '2024-11-30', '', 'Include new skills learned in recent workshops', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16'),

('Calibrate lab equipment for experiment', 'Ensure all sensors and devices are properly calibrated for upcoming tests', 'Work', 'Y', 'N', 'ToDo', '0%', '2024-10-18', 'project', 'Double-check the spectrometer settings', 'h7user1@gmail.com', '2024-10-16', 'h7user1@gmail.com', '2024-10-16');