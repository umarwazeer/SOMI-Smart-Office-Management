<template>
  <div class="camera-page q-pa-md">
    <q-card class="camera-card">
      <q-card-section class="camera-header">
        <div>
          <div class="text-overline">BIOMETRIC WORKSPACE</div>
          <div class="text-h5 text-weight-bold">Camera Capture</div>
          <div class="text-caption camera-subtitle">
            Capture a clear employee image for future face-attendance workflows.
          </div>
        </div>

        <q-icon
          :name="cameraActive ? 'videocam' : 'videocam_off'"
          size="32px"
          :class="cameraActive ? 'text-positive' : 'text-grey-6'"
        />
      </q-card-section>

      <q-separator />

      <q-card-section class="camera-content">
        <div v-if="errorMessage" class="error-box q-mb-md">
          <q-icon name="error_outline" size="22px" />
          <div>
            <div class="text-weight-medium">Camera unavailable</div>
            <div class="text-caption">{{ errorMessage }}</div>
          </div>
        </div>

        <div
          v-if="!capturedImage"
          class="camera-preview"
          :class="{ 'camera-preview--inactive': !cameraActive }"
        >
          <video
            ref="video"
            autoplay
            playsinline
            muted
            class="camera-video"
          />

          <div v-if="!cameraActive && !errorMessage" class="camera-placeholder">
            <q-spinner v-if="startingCamera" size="38px" />
            <q-icon v-else name="videocam_off" size="52px" />
            <div class="text-subtitle1 q-mt-md">
              {{ startingCamera ? 'Starting camera...' : 'Camera is off' }}
            </div>
          </div>

          <div v-if="cameraActive" class="camera-frame">
            <span class="corner corner-tl"></span>
            <span class="corner corner-tr"></span>
            <span class="corner corner-bl"></span>
            <span class="corner corner-br"></span>
          </div>
        </div>

        <div v-else class="captured-preview">
          <img :src="capturedImage" alt="Captured employee" />
          <div class="captured-badge">
            <q-icon name="check_circle" size="18px" />
            Image captured
          </div>
        </div>

        <canvas ref="canvas" class="hidden-canvas"></canvas>

        <div class="camera-actions q-mt-lg">
          <template v-if="!capturedImage">
            <q-btn
              v-if="!cameraActive"
              unelevated
              color="primary"
              icon="videocam"
              label="Start Camera"
              class="action-btn"
              :loading="startingCamera"
              @click="startCamera"
            />

            <q-btn
              v-else
              unelevated
              color="primary"
              icon="photo_camera"
              label="Capture Image"
              class="action-btn"
              @click="captureImage"
            />

            <q-btn
              v-if="cameraActive"
              flat
              icon="videocam_off"
              label="Stop"
              class="secondary-btn"
              @click="stopCamera"
            />
          </template>

          <template v-else>
            <q-btn
              outline
              color="primary"
              icon="refresh"
              label="Retake"
              class="action-btn"
              @click="retakeImage"
            />

            <q-btn
              unelevated
              color="positive"
              icon="check"
              label="Use Image"
              class="action-btn"
              @click="confirmImage"
            />
          </template>
        </div>

        <div class="camera-info q-mt-lg">
          <q-icon name="info_outline" size="18px" />
          <span>
            For best results, use good lighting and keep the employee's face
            centered in the frame.
          </span>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'CameraCapture',

  emits: ['image-captured'],

  data() {
    return {
      stream: null,
      cameraActive: false,
      startingCamera: false,
      capturedImage: '',
      errorMessage: '',
    }
  },

  mounted() {
    this.startCamera()
  },

  beforeUnmount() {
    this.stopCamera()
  },

  methods: {
    async startCamera() {
      if (this.cameraActive || this.startingCamera) {
        return
      }

      this.startingCamera = true
      this.errorMessage = ''

      try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          throw new Error('Camera access is not supported by this browser.')
        }

        this.stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: 'user',
            width: {
              ideal: 1280,
            },
            height: {
              ideal: 720,
            },
          },
          audio: false,
        })

        const video = this.$refs.video

        if (!video) {
          throw new Error('Camera preview could not be initialized.')
        }

        video.srcObject = this.stream

        await video.play()

        this.cameraActive = true
      } catch (error) {
        console.error('Camera access error:', error)

        this.errorMessage = this.getCameraErrorMessage(error)
        this.cameraActive = false
        this.stopMediaStream()
      } finally {
        this.startingCamera = false
      }
    },

    stopCamera() {
      this.stopMediaStream()
      this.cameraActive = false
    },

    stopMediaStream() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop())
        this.stream = null
      }

      const video = this.$refs.video

      if (video) {
        video.srcObject = null
      }
    },

    captureImage() {
      const video = this.$refs.video
      const canvas = this.$refs.canvas

      if (!video || !canvas || !this.cameraActive) {
        return
      }

      const width = video.videoWidth || 1280
      const height = video.videoHeight || 720

      canvas.width = width
      canvas.height = height

      const context = canvas.getContext('2d')

      if (!context) {
        this.errorMessage = 'Unable to process the camera image.'
        return
      }

      context.drawImage(video, 0, 0, width, height)

      this.capturedImage = canvas.toDataURL('image/jpeg', 0.9)

      this.stopCamera()
    },

    retakeImage() {
      this.capturedImage = ''
      this.errorMessage = ''
      this.startCamera()
    },

    confirmImage() {
      if (!this.capturedImage) {
        return
      }

      this.$emit('image-captured', this.capturedImage)
    },

    getCameraErrorMessage(error) {
      if (!error) {
        return 'Unable to access the camera.'
      }

      if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
        return 'Camera permission was denied. Please allow camera access in your browser settings.'
      }

      if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
        return 'No camera device was found on this computer.'
      }

      if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
        return 'The camera is already being used by another application.'
      }

      return error.message || 'Unable to access the camera.'
    },
  },
}
</script>

<style scoped>
.camera-page {
  width: 100%;
  min-height: 100%;
}

.camera-card {
  width: 100%;
  max-width: 760px;
  margin: 0 auto;
  border-radius: 18px;
  overflow: hidden;
}

.camera-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.camera-subtitle {
  margin-top: 4px;
  opacity: 0.72;
}

.camera-content {
  padding: 24px;
}

.camera-preview,
.captured-preview {
  position: relative;
  width: 100%;
  max-width: 680px;
  margin: 0 auto;
  aspect-ratio: 16 / 9;
  border-radius: 16px;
  overflow: hidden;
  background: #101418;
}

.camera-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.camera-preview--inactive {
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.72);
  text-align: center;
}

.camera-frame {
  position: absolute;
  inset: 10%;
  pointer-events: none;
}

.corner {
  position: absolute;
  width: 42px;
  height: 42px;
  border-style: solid;
  border-width: 0;
}

.corner-tl {
  top: 0;
  left: 0;
  border-top-width: 3px;
  border-left-width: 3px;
}

.corner-tr {
  top: 0;
  right: 0;
  border-top-width: 3px;
  border-right-width: 3px;
}

.corner-bl {
  bottom: 0;
  left: 0;
  border-bottom-width: 3px;
  border-left-width: 3px;
}

.corner-br {
  right: 0;
  bottom: 0;
  border-right-width: 3px;
  border-bottom-width: 3px;
}

.captured-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.captured-badge {
  position: absolute;
  left: 16px;
  bottom: 16px;
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 12px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.68);
  color: white;
  font-size: 13px;
  font-weight: 600;
}

.camera-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.action-btn {
  min-width: 150px;
  min-height: 44px;
  border-radius: 10px;
}

.secondary-btn {
  min-height: 44px;
}

.error-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 12px;
  background: rgba(198, 40, 40, 0.1);
  color: #c62828;
}

.camera-info {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-size: 13px;
  opacity: 0.7;
}

.hidden-canvas {
  display: none;
}

@media (max-width: 600px) {
  .camera-content {
    padding: 16px;
  }

  .camera-header {
    align-items: flex-start;
  }

  .camera-header .text-h5 {
    font-size: 20px;
  }

  .camera-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .action-btn,
  .secondary-btn {
    width: 100%;
  }

  .camera-preview,
  .captured-preview {
    aspect-ratio: 4 / 3;
  }
}

.body--dark .camera-card {
  background: #171b21;
}

.body--dark .camera-subtitle {
  color: rgba(255, 255, 255, 0.7);
}

.body--dark .error-box {
  color: #ff8a80;
}
</style>
