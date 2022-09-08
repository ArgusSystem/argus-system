# Argus System

## Abstract

Argus is a distributed system designed for camera surveillance. In particular, Argus aims to:
- Process video from multiple sources in _realtime_<sup>[1]<sup>.
- Detect and classify people in the video streams.
- Implement custom rules based on the detection to enhance security and tracing. These rules
include:
  - Add roles to the people registered in the system.
  - Notify when someone is in a particular set of spots.
  - Create spots only available for certain people on a certain time of the day.
  - Count people on a certain location.
- Send notification alerts for privileged users.
- View the history of a registered person.
- Add and remove people from the tracking system.

The rules' subsystem is described in a general and broad way in order to prioritize flexibility.
Some real use cases for the rules' system might be:
  - Search for someone that is missing.
  - Ban people from entering an area.
  - Alert when someone unknown to the system is in the area.
  - Allow only authorized people on an area. The area may be available for everyone during working
  hours but only available for security during the night.
  - Keep track of someone we care, for example children or elderly people.
  - Restrict the number of people on a certain area, for example due to COVID-19.

<sup>_[1] A video is processed in realtime if all the processing is bounded by a threshold P. To
reproduce the video as a continuous stream, we need a fix delay equal to the video length plus the
processing threshold. In this implementation, we will use a threshold of 10 seconds._<sup>

## Web application

The web application will be the main interface to interact with the system. Only authorized users 
can use it. The features available include:
- View from a camera, including the detection and classification of people.
- Alerts triggered, sorted by time and priority. The alerts can show footage of the camera with the
reason for the notification.
- Management panel, to add, modify or remove a person from the classification system.
- History from a person of the system, detailing the last times it was viewed by the system.

## Mobile application

The android application works as a secondary interface for the users to interact with the system.
It allows the user to:
- View a map of the area, with all the people in the system. The filters can limit the data shown by:
  - Person, to check the tracking history.
  - Time, to limit to particular time frame.
  - Access rules, to check areas with a particular rule.
- Alert dashboard, to view all the alerts triggered in the system. Can be filtered and sorted by 
time and priority.
- For some users, the possibility to allow a certain person in the system to an area they own for
a limited period of time.

### Use case: Private Residential Area

For the particular case of a private residential area, we defined the following roles, 
areas and access rules:

- Roles:
  - Resident
  - Guest
  - Staff
  - Security
- Areas:
  - Private areas, like residential houses or private events in a common area.
  - Public areas, like streets, parks, restaurants and shared spaces<sup>[2].
  - Limited areas, like _staff only_ rooms in public areas.
  - Unauthorized areas, like security rooms.
- Access rules:
  - Free: the person is in a permitted area and triggers no alerts.
  - Suspicious: the person may be in a permitted area depending on the context,
triggers a low-priority alert.
  - Unauthorized: the person is in an unauthorized area and triggers a high 
priority alert.

These access rules will limit the use of areas depending on the roles:
  - Guests have free access to a residential house and public places but all other areas are 
unauthorized.
  - Residents have free access to a residential house and public places, suspicious access to other
residential house and limited areas and can't access unauthorized areas.
  - Maintenance staff can access public and limited areas but are suspicious in private areas and
can't enter unauthorized areas.
  - Security staff has free access to public areas, limited areas and security areas, but may be
suspicious on private areas.

<sup>[2] Some public areas may become unauthorized depending on the time. For example,
a restaurant will be public only during working hours.<sup>



# Argus System

## Abstract

Argus is a distributed system designed for camera surveillance. In particular, Argus aims to:
- Process video from multiple sources in _realtime_<sup>[1]<sup>.
- Detect and classify people in the video streams.
- Implement custom rules based on the detection to enhance security and tracing. These rules
include:
  - Add roles to the people registered in the system.
  - Notify when someone is in a particular set of spots.
  - Create spots only available for certain people on a certain time of the day.
  - Count people on a certain location.
- Send notification alerts for privileged users.
- View the history of a registered person.
- Add and remove people from the tracking system.

The rules' subsystem is described in a general and broad way in order to prioritize flexibility.
Some real use cases for the rules' system might be:
  - Search for someone that is missing.
  - Ban people from entering an area.
  - Alert when someone unknown to the system is in the area.
  - Allow only authorized people on an area. The area may be available for everyone during working
  hours but only available for security during the night.
  - Keep track of someone we care, for example children or elderly people.
  - Restrict the number of people on a certain area, for example due to COVID-19.

<sup>_[1] A video is processed in realtime if all the processing is bounded by a threshold P. To
reproduce the video as a continuous stream, we need a fix delay equal to the video length plus the
processing threshold. In this implementation, we will use a threshold of 10 seconds._<sup>

## Web application

The web application will be the main interface to interact with the system. Only authorized users 
can use it. The features available include:
- View from a camera, including the detection and classification of people.
- Alerts triggered, sorted by time and priority. The alerts can show footage of the camera with the
reason for the notification.
- Management panel, to add, modify or remove a person from the classification system.
- History from a person of the system, detailing the last times it was viewed by the system.

## Mobile application

The android application works as a secondary interface for the users to interact with the system.
It allows the user to:
- View a map of the area, with all the people in the system. The filters can limit the data shown by:
  - Person, to check the tracking history.
  - Time, to limit to particular time frame.
  - Access rules, to check areas with a particular rule.
- Alert dashboard, to view all the alerts triggered in the system. Can be filtered and sorted by 
time and priority.
- For some users, the possibility to allow a certain person in the system to an area they own for
a limited period of time.

### Use case: Private Residential Area

For the particular case of a private residential area, we defined the following roles, 
areas and access rules:

- Roles:
  - Resident
  - Guest
  - Staff
  - Security
- Areas:
  - Private areas, like residential houses or private events in a common area.
  - Public areas, like streets, parks, restaurants and shared spaces<sup>[2].
  - Limited areas, like _staff only_ rooms in public areas.
  - Unauthorized areas, like security rooms.
- Access rules:
  - Free: the person is in a permitted area and triggers no alerts.
  - Suspicious: the person may be in a permitted area depending on the context,
triggers a low-priority alert.
  - Unauthorized: the person is in an unauthorized area and triggers a high 
priority alert.

These access rules will limit the use of areas depending on the roles:
  - Guests have free access to a residential house and public places but all other areas are 
unauthorized.
  - Residents have free access to a residential house and public places, suspicious access to other
residential house and limited areas and can't access unauthorized areas.
  - Maintenance staff can access public and limited areas but are suspicious in private areas and
can't enter unauthorized areas.
  - Security staff has free access to public areas, limited areas and security areas, but may be
suspicious on private areas.

<sup>[2] Some public areas may become unauthorized depending on the time. For example,
a restaurant will be public only during working hours.<sup>
