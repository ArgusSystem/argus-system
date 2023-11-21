SELECT camera, severity, restriction, min(TIMESTAMP) AS start_time, max(TIMESTAMP) AS end_time
FROM (
    SELECT timestamp, camera, restriction, severity, count(is_reset) OVER (ORDER BY camera, timestamp) AS grp
    FROM (
        SELECT timestamp,
               camera,
               restriction,
               severity,
               CASE WHEN lag(camera) OVER (ORDER BY camera, timestamp) <> camera
                         OR lag(severity) OVER (ORDER BY camera, timestamp) <> severity
                         OR timestamp - lag(timestamp) OVER (ORDER BY camera, timestamp) > 30000
                   THEN 1 END as is_reset
        FROM (SELECT camera.id                                        as camera,
                     face.timestamp                                   as timestamp,
                     COALESCE(restriction.id, -1)                     as restriction,
                     COALESCE(restrictionseverity.name, '')           as severity
              FROM face
              LEFT JOIN videochunk ON face.video_chunk_id = videochunk.id
              LEFT JOIN camera ON videochunk.camera_id = camera.id
              LEFT JOIN brokenrestriction ON brokenrestriction.face_id = face.id
              LEFT JOIN restriction ON brokenrestriction.restriction_id = restriction.id
              LEFT JOIN restrictionseverity ON restriction.severity_id = restrictionseverity.id
              WHERE NOT is_match
              ORDER BY camera, timestamp
              ) AS tmp
        ) AS t
    ) AS G
GROUP BY camera, restriction, severity, grp
ORDER BY end_time;