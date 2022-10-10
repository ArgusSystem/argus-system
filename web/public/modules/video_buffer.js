const MIME = 'video/mp4; codecs="avc1.f4001f"';

export class VideoBuffer {
    constructor(mediaSource) {
        this.sourceBuffer = mediaSource.addSourceBuffer(MIME);
        this.sourceBuffer.mode = 'sequence';

        this.sourceBuffer.addEventListener('error', function (e) {
            console.log(e);
        });

        this.chunksMetadata = [];
    }

    append(chunk) {
        this.sourceBuffer.appendBuffer(chunk.payload);
        this.chunksMetadata.push(chunk);
    }

    currentChunk(time) {
        let chunk_duration = this.chunksMetadata[0].duration;
        // OJO esto funciona solo si todos los chunks tienen la misma duracion
        let chunk_index = Math.floor(time / chunk_duration);
        let chunk_id = this.chunksMetadata[chunk_index].video_chunk_id;

        let sampling_rate = this.chunksMetadata[chunk_index].sampling_rate;
        let frame_rate = this.chunksMetadata[chunk_index].framerate;

        let time_in_current_chunk = (time - Math.floor(time / chunk_duration) * chunk_duration);
        let current_frame = Math.floor(time_in_current_chunk * frame_rate);

        let samples_per_chunk = Math.floor(chunk_duration * sampling_rate);
        let frames_between_samples = Math.round(frame_rate / sampling_rate);
        let hold_0_offset = -1;
        let next_offset = -1;

        // we iterate the sampled frame offsets for this video chunk
        for (let sample_index = 0; sample_index < samples_per_chunk; ++sample_index) {
            // IMPORTANTE: la logica que calcula los sample frame offsets tiene que ser la misma que en python
            // sino se podria incluir en el VideoChunkMessage los offsets de los frames sampleados
            let sampled_frame_offset = Math.round(frames_between_samples / 2) + sample_index * frames_between_samples;
            if (sampled_frame_offset > current_frame) {
                if (hold_0_offset === -1) {
                    // the current frame is earlier than the first sampled frame from this chunk
                    // so we use the last sampled frame from the previous chunk
                    if (chunk_index - 1 > 0) {
                        chunk_id = this.chunksMetadata[chunk_index - 1].video_chunk_id;
                        hold_0_offset = Math.round(frames_between_samples / 2) + (samples_per_chunk - 1) * frames_between_samples;
                    }
                }
                break;
            }
            hold_0_offset = sampled_frame_offset;
        }
        return [chunk_id, hold_0_offset];
    }
}
