SELECT camera, person, severity, restriction, min(TIMESTAMP) AS start_time,  max(TIMESTAMP) AS end_time
FROM (
    SELECT timestamp, camera, person, restriction, severity, count(is_reset) OVER (ORDER BY person, timestamp, camera) AS grp
    FROM (
        SELECT timestamp,
               camera,
               person,
               restriction,
               severity,
               CASE WHEN lag(camera) OVER (ORDER BY person, timestamp, camera) <> camera
                         OR lag(person) OVER (ORDER BY person, timestamp, camera) <> person
                         OR lag(severity) OVER (ORDER BY person, timestamp, camera) <> severity
                   THEN 1 END as is_reset
        FROM (SELECT camera.id                                        as camera,
                     face.person_id                                   as person,
                     face.timestamp                                   as timestamp,
                     COALESCE(restriction.id, -1)                     as restriction,
                     COALESCE(restrictionseverity.name, '')           as severity
              FROM face
              LEFT JOIN videochunk ON face.video_chunk_id = videochunk.id
              LEFT JOIN camera ON videochunk.camera_id = camera.id
              LEFT JOIN brokenrestriction ON brokenrestriction.face_id = face.id
              LEFT JOIN restriction ON brokenrestriction.restriction_id = restriction.id
              LEFT JOIN restrictionseverity ON restriction.severity_id = restrictionseverity.id
              WHERE is_match
              ORDER BY person, timestamp, camera
              ) AS tmp
        ) AS t
    ) AS G
GROUP BY camera, person, restriction, severity, grp
ORDER BY person, end_time;