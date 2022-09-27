// Asserts
const assert = require('assert')

// S3 Client
const Minio = require('minio')
const minioClient = new Minio.Client( {
  endPoint: 'localhost',
  port: 9500,
  useSSL: false,
  accessKey: 'fiubrother',
  secretKey: 'alwayswatching'
})

// PG Client
const { Client } = require('pg')
const pgClient = new Client({
  host: 'localhost',
  database: 'big_fiubrother',
  user: 'fiubrother',
  password: 'alwayswatching',
  port: 5432
})

pgClient.connect()

// CREATE DATABASE RECORDS
const createVideoChunkQuery = `
  INSERT INTO video_chunk (camera_id, timestamp, frame_count, duration_ms, processed)
  VALUES ('CAMERA_ID_1', 1.0, 119, 4959, TRUE)
  RETURNING id;
`

const createFrameQuery = `
  INSERT INTO frame ("offset", video_chunk_id)
  VALUES ($1, $2)
  RETURNING id;
`

const createPersonQuery = `
  INSERT INTO person (name)
  VALUES ('John Doe')
  RETURNING id;
`

const createFaceQuery = `
  INSERT INTO face (frame_id, bounding_box, classification_id, probability_classification, is_match)
  VALUES ($1, '[500, 500, 100, 100]', $2, $3, TRUE)
  RETURNING id;
`

pgClient.query(createVideoChunkQuery, []).then((chunk_res) => {
  const chunkId  = chunk_res.rows[0].id
  console.log(chunkId)

  pgClient.query(createPersonQuery, []).then((person_res) => {
    const personId  = person_res.rows[0].id

    for (let i = 0; i < 119; i+=24) {
      pgClient.query(createFrameQuery, [i, chunkId]).then((frame_res) => {
        const frameId  = frame_res.rows[0].id

        pgClient.query(createFaceQuery, [frameId, personId, 80.0 + (i/12.0)])
      })
    }
  })

  // UPLOAD VIDEO CHUNK TO S3
  const filepath = 'resources/test_chunk.mp4'

  minioClient.fPutObject('video-chunks', `${chunkId}.mp4` , filepath, {}, function(err, etag) {
    return console.log(err, etag) // err should be null
  })
})


// CLIENT SOCKET
const io = require('socket.io-client')

const socketClient = io.connect('http://localhost:8080/video', { forceNew: true })

socketClient.on("chunk", (chunk) => {
  assert(chunk.id > 0)
  assert(chunk.frameCount === 119)
  assert(chunk.duration === 4959)
  assert(chunk.timestamp === 1)
  assert(chunk.payload.length === 1791908)
  console.log(`Assertions successful for video chunk ${chunk.id}`)
})

socketClient.on("analysis", (analysis) => {
  assert(analysis.chunkId > 0)
  assert(analysis.frameCount === 119)
  assert(analysis.frames.length === 5)

  for (let i = 0; i < 5; i++) {
    const frame = analysis.frames[i]
    assert(frame.offset === i * 24)
    assert(frame.faces.length === 1)

    const face = frame.faces[0]
    assert(face.isMatch)
    assert(face.probability === 80 + i * 2)
    assert(face.name === 'John Doe')
    assert(JSON.stringify(face.box) === JSON.stringify([500, 500, 100, 100]))
    console.log(`Assertions successful for video analysis ${analysis.chunkId}`)
  }
})