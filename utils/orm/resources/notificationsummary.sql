SELECT user_id,
       camera AS camera_id,
       person AS person_id,
       person = -1 AS is_unknown,
       restriction AS restriction_id,
       severity,
       start_time,
       end_time,
       bool_or("read") AS "read",
       array_agg(notification.id) AS notification_ids
FROM notification
LEFT JOIN brokenrestriction ON broken_restriction_id = brokenrestriction.id
LEFT JOIN face ON face_id = face.id
LEFT JOIN videochunk ON video_chunk_id = videochunk.id
LEFT JOIN
    (SELECT * FROM
        (SELECT camera, -1 AS person, severity, restriction, start_time, end_time FROM unknownsighting) as unknownsightingperson
        UNION
        (SELECT * from sighting)
    ) AS allsightings
    ON camera = camera_id
    AND restriction_id = restriction
    AND face.timestamp <= end_time
    AND face.timestamp >= start_time
    AND ( (is_match AND person = person_id) OR ((not is_match) AND person = -1) )
GROUP BY user_id, camera, person, restriction, severity, start_time, end_time