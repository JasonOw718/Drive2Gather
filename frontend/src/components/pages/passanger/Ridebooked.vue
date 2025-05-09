<template>
  <div ref="containerRef" class="min-h-screen flex flex-col justify-between items-center bg-white px-4 pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)]" style="max-width: 420px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
    <!-- Car Icon with Animation -->
    <div class="w-full flex items-start mt-10 mb-6 relative h-24">
      <img
        :key="isAccepted"
        :class="['w-28 h-20 object-contain', isAccepted ? 'car-animate' : '']"
        :style="carStyle"
        src="/src/assets/images/caricon.jpg"
        alt="Car Icon"
      />
    </div>

    <!-- Status Text -->
    <div class="relative w-full min-h-[3.5rem]">
      <transition name="slide-left" mode="out-in">
        <div
          :key="isAccepted ? 'accepted' : 'pending'"
          class="text-xl font-medium transition-colors duration-700 text-left w-full absolute left-0 top-0"
          :style="{
            color: isAccepted ? '#C77DFF' : '#303030',
            fontFamily: 'Roboto, sans-serif',
            lineHeight: '2.5rem'
          }"
        >
          {{ isAccepted ? 'Booked! Your Ride has been confirmed!' : 'Booked! Your Ride has been requested, Please wait for the driver to accept.' }}
        </div>
      </transition>
    </div>

    <!-- Message -->
    <div class="text-base text-[#8C8C8C] font-normal mt-16 mb-2 text-left w-full" style="font-family: 'Roboto', sans-serif;">
      Your driver will wait only 5 minutes.
    </div>

    <!-- Spacer -->
    <div class="flex-1"></div>

    <!-- View Ride Button -->
    <button
      class="w-full py-3 px-4 rounded-full shadow-md text-base font-bold transition-all duration-300 mb-2"
      :class="isAccepted ? 'bg-[#C77DFF] text-white hover:bg-opacity-90 cursor-pointer' : 'bg-gray-300 text-gray-400 cursor-not-allowed'"
      :disabled="!isAccepted"
      style="max-width: 100%; font-family: 'Roboto', sans-serif;"
      @click="goToOtwpage"
    >
      View Ride
    </button>

    <!-- Demo: Toggle isAccepted -->
    <button class="mt-4 text-xs underline text-[#C77DFF]" @click="toggleAccepted">
      Toggle Driver Acceptance (Demo)
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const isAccepted = ref(false)
const animationCounter = ref(0)
const containerRef = ref(null)
const carWidth = 112 // 28 * 4 (tailwind w-28 is 7rem = 112px)
const safeMargin = 16 // px
const maxTranslateX = ref(0)
const outTranslateX = ref(0)
const router = useRouter()

const updateMaxTranslateX = () => {
  if (containerRef.value) {
    const containerWidth = containerRef.value.offsetWidth
    maxTranslateX.value = Math.max(containerWidth - carWidth - safeMargin, 0)
    outTranslateX.value = Math.max(containerWidth + carWidth, 0) // move fully out of screen
  }
}

onMounted(() => {
  updateMaxTranslateX()
  window.addEventListener('resize', updateMaxTranslateX)
})

watch(containerRef, updateMaxTranslateX)

const carStyle = computed(() => {
  if (isAccepted.value) {
    return {
      animation: `car-slide-dynamic-${animationCounter.value} 2.5s linear infinite`,
      '--max-x': `${maxTranslateX.value}px`,
      '--out-x': `${outTranslateX.value}px`,
      '--car-width': `${carWidth}px`
    }
  }
  return {}
})

function toggleAccepted() {
  isAccepted.value = !isAccepted.value
  if (isAccepted.value) {
    animationCounter.value++
    // Dynamically inject new keyframes for each animation name
    nextTick(() => {
      const styleId = `car-slide-dynamic-${animationCounter.value}`
      if (!document.getElementById(styleId)) {
        const style = document.createElement('style')
        style.id = styleId
        style.innerHTML = `
          @keyframes car-slide-dynamic-${animationCounter.value} {
            0% { transform: translateX(calc(-1 * var(--car-width, 112px))); opacity: 0; }
            5% { opacity: 1; }
            90% { transform: translateX(var(--max-x, 120px)); opacity: 1; }
            100% { transform: translateX(var(--out-x, 200vw)); opacity: 0; }
          }
        `
        document.head.appendChild(style)
      }
    })
  }
}

function goToOtwpage() {
  if (isAccepted.value) {
    router.push({ name: 'Otwpage' })
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.car-animate {
  /* animation is set dynamically via style binding */
}

.slide-left-enter-active, .slide-left-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  width: 100%;
}
.slide-left-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}
.slide-left-enter-to {
  opacity: 1;
  transform: translateX(0);
}
.slide-left-leave-from {
  opacity: 1;
  transform: translateX(0);
}
.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}
</style>
