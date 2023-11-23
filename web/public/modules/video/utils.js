export function createVideoElement(camera, scalingFactor) {
    const htmlVideoElement = document.createElement('video');

    htmlVideoElement.id = `video-${camera.name}`;
    htmlVideoElement.width = camera.width / scalingFactor;
    htmlVideoElement.height = camera.height / scalingFactor;
    htmlVideoElement.hidden = true;
    htmlVideoElement.muted = true;

    return htmlVideoElement;
}

export function createCanvasElement(camera, scalingFactor) {
    const htmlCanvasElement = document.createElement('canvas');

    htmlCanvasElement.id = `canvas-${camera.name}`;
    htmlCanvasElement.width = camera.width / scalingFactor;
    htmlCanvasElement.height = camera.height / scalingFactor;

    return htmlCanvasElement;
}

export function calculateScalingFactor(cameras) {
   let scalingFactor = 1;

   while ((scalingFactor ** 2) < cameras){
       scalingFactor += 1;
   }

   return scalingFactor;
}