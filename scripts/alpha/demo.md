# Demo - Alpha 0.5.0 

## Before meeting

1. Start platform services docker environments
2. Run _alpha_setup_ script
3. Start Argus applications (1 of each)
   1. Sampler
   2. Detector
   3. Classifier
   4. Warden
   5. Notifier
   6. Web Streamer
   7. Web API
4. Run all streams together
5. Clean with stream database (ONLY_CLEAN: _True_)
6. Change CLEAN_ONLY to _False_
7. Go to the Home tab

## Demo

### Edu's computer

1. Show set-up
   1. People
   2. Areas
   3. Restrictions
2. Go to Live Feed -> All-Cameras View
3. Start _stream_database_ script
   1. Show notifications popping up on the right
4. Show Notifications tab (10)
5. Show History tab
6. Show unknown faces
   1. Run clustering task
   2. Re tag all clusters (Everything except outliers)

### Gabo's computer

1. Go back to Live Feed -> All-Cameras View
2. Re-run _stream_database_
   1. Show lees notifications popping up
3. Show Notifications tab
4. Show statistics