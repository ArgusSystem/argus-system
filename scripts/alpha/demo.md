# Demo - Alpha 0.5.0 

## Before meeting

1. Start platform services docker environments
2. Clean with stream database (ONLY_CLEAN: _True_)
3. Start Argus applications (1 of each)
   1. Sampler
   2. Detector
   3. Classifier
   4. Warden
   5. Notifier
   6. Web Streamer
   7. Web API
4. Change CLEAN_ONLY to _False_
5. Go to Home tab

## Demo

1. Show set-up
   1. People
   2. Areas
   3. Restrictions
2. Go to Live Feed -> All-Cameras View
3. Start _stream_database_ script
   1. Show notifications popping up on the right
4. Show Notifications tab
5. Show History tab
6. Show unknown faces
   1. Run clustering task
   2. Re tag all clusters (Outliers must have 69 pics at the end)
7. Go back to Live Feed -> All-Cameras View
8. Re-run _stream_database_
   1. Show lees notifications popping up
9. Show Notifications tab
10. Show statistics