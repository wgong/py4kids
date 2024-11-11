-- Assuming TABLE_H7_TASK is 'habits7_task'
-- Assuming the current date is 'DATA_DATE' for created_at and updated_at
-- Assuming 'USERNAME' as the user for created_by and updated_by

INSERT INTO habits7_task (task_name, description, task_group, is_urgent, is_important, status, pct_completed, due_date, task_type, note, created_by, created_at, updated_by, updated_at)
VALUES 
('Submit conference paper on deep learning', 'Finalize and submit the paper on recent deep learning advancements', 'Work', 'Y', 'Y', 'Doing', '75%', '2024-11-01', 'research', 'Remember to include latest experimental results', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Prepare for AI ethics seminar presentation', 'Create slides and talking points for the upcoming ethics in AI seminar', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-11-15', 'learning', 'Focus on recent controversies in AI applications', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Debug neural network model', 'Identify and fix issues in the current neural network implementation', 'Work', 'Y', 'Y', 'Doing', '50%', '2024-10-20', 'project', 'Check for overfitting in the validation set', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Grocery shopping', 'Buy essentials for the week', 'Personal', 'Y', 'N', 'ToDo', '0%', '2024-10-18', '', 'Remember to buy vegetables and fruits', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Review latest papers on reinforcement learning', 'Read and summarize recent advancements in RL', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-10-30', 'learning', 'Focus on papers from top conferences like NeurIPS and ICML', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Schedule dentist appointment', 'Book a check-up with Dr. Smith', 'Personal', 'N', 'N', 'ToDo', '0%', '2024-11-30', '', 'Ask about wisdom tooth extraction', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Meet with thesis advisor', 'Discuss progress and next steps for PhD thesis', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-19', 'research', 'Prepare summary of recent experiments', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Prepare dataset for machine learning experiment', 'Clean and preprocess data for the next ML model', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-10-25', 'project', 'Ensure proper normalization and feature scaling', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Plan weekend hike', 'Organize a hike with friends for the coming weekend', 'Personal', 'N', 'N', 'ToDo', '0%', '2024-10-21', 'fun', 'Check weather forecast and trail conditions', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Submit progress report to department', 'Compile and submit monthly PhD progress report', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-31', 'project', 'Include summary of recent paper submissions and experiment results', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Attend friend''s birthday party', 'Celebrate with friends at John''s birthday party', 'Personal', 'Y', 'N', 'ToDo', '0%', '2024-10-22', 'fun', 'Don''t forget to bring a gift', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Optimize code for GPU acceleration', 'Refactor current codebase to utilize GPU more efficiently', 'Work', 'N', 'Y', 'ToDo', '0%', '2024-11-10', 'project', 'Focus on the most computationally intensive parts first', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Pay rent', 'Transfer monthly rent to landlord', 'Personal', 'Y', 'Y', 'ToDo', '0%', '2024-10-31', '', 'Set up automatic payment for future months', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Write blog post on recent AI breakthroughs', 'Summarize and explain recent advancements in AI for the lab blog', 'Work', 'N', 'N', 'ToDo', '0%', '2024-11-15', 'research', 'Include insights from the latest conference', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Exercise at gym', 'Complete weekly workout routine', 'Personal', 'N', 'Y', 'ToDo', '0%', '2024-10-20', '', 'Focus on cardio and upper body this week', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Prepare for teaching assistant duties', 'Review material and prepare for upcoming TA session', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-18', 'learning', 'Create practice problems for students', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Call parents', 'Weekly check-in call with family', 'Personal', 'N', 'Y', 'ToDo', '0%', '2024-10-20', '', 'Update them on recent research progress', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Attend research group meeting', 'Participate in weekly lab meeting and present recent findings', 'Work', 'Y', 'Y', 'ToDo', '0%', '2024-10-17', 'research', 'Prepare slides on the latest experiment results', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Update CV', 'Add recent publications and projects to curriculum vitae', 'Personal', 'N', 'N', 'ToDo', '0%', '2024-11-30', '', 'Include new skills learned in recent workshops', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE'),

('Calibrate lab equipment for experiment', 'Ensure all sensors and devices are properly calibrated for upcoming tests', 'Work', 'Y', 'N', 'ToDo', '0%', '2024-10-18', 'project', 'Double-check the spectrometer settings', 'USERNAME', 'DATA_DATE', 'USERNAME', 'DATA_DATE');