<template>
	<div class="max-w-md mx-auto w-full p-4">
		<h2 class="text-xl mb-4">Convert Audio</h2>

		<form @submit.prevent="onSubmit" class="space-y-4">
			<div v-if="!previewUrl">
				<div
					@dragover.prevent="isDragActive = true"
					@dragleave.prevent="isDragActive = false"
					@drop.prevent="onDrop"
					:class="['relative w-full h-64 flex items-center justify-center rounded border-2 border-dashed cursor-pointer transition-colors', isDragActive ? 'border-green-400 bg-green-50' : 'border-gray-300 bg-white']"
				>
					<input
						ref="fileInput"
						type="file"
						accept="audio/*"
						class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
						@change="onFileChange"
					/>
					<p class="text-gray-500 text-center px-4">
						Click or drag & drop an audio file here
					</p>
				</div>
			</div>

			<div v-else class="relative mt-4 w-full h-64 border-2 border-dashed rounded bg-white flex flex-col items-center justify-center">
				<button
					@click="clearFile"
					type="button"
					class="absolute top-2 right-2 z-10 bg-gray-800 bg-opacity-50 hover:bg-opacity-75 text-white rounded-full p-1 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
					aria-label="Clear audio"
					:disabled="isLoading"
				>
					<XMarkIcon class="h-4 w-4"/>
				</button>

				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-12 w-12 text-gray-500"
					viewBox="0 0 20 20"
					fill="currentColor"
				>
					<path d="M11 5L6 9H2v6h4l5 4V5z"/>
				</svg>

				<audio
					:src="previewUrl"
					controls
					class="mt-2 w-3/4"
				/>
			</div>

			<select v-model="format" class="w-full border rounded p-2">
				<option
					v-for="opt in formats"
					:key="opt.value"
					:value="opt.value"
				>
					{{ opt.label }}
				</option>
			</select>

			<button
				type="submit"
				:disabled="!file || isLoading"
				class="w-full bg-green-600 text-white py-2 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
			>
				{{ isLoading ? 'Converting...' : 'Convert' }}
			</button>
		</form>
	</div>
</template>

<script lang="ts" setup>
import { ref, onUnmounted } from 'vue'
import { convertAudio } from '@/services/converterApi'
import XMarkIcon from '@/components/icons/XMarkIcon.vue'

interface FormatOption {
	value: string
	label: string
}

const file = ref<File | null>(null)
const previewUrl = ref<string | null>(null)
const isDragActive = ref(false)
const format = ref<string>('mp3')
const fileInput = ref<HTMLInputElement | null>(null)
const isLoading = ref(false)

const formats = <FormatOption[]>[
	{ value: 'wav', label: 'WAV' },
	{ value: 'mp3', label: 'MP3' },
	{ value: 'ogg', label: 'OGG' },
	{ value: 'flac', label: 'FLAC' },
]

function setFile(f: File) {
	if (previewUrl.value) {
		URL.revokeObjectURL(previewUrl.value)
	}
	file.value = f
	previewUrl.value = URL.createObjectURL(f)
}

function onFileChange(e: Event) {
	const input = e.target as HTMLInputElement
	if (input.files && input.files[0] && input.files[0].type.startsWith('audio/')) {
		setFile(input.files[0])
	}
}

function onDrop(e: DragEvent) {
	isDragActive.value = false
	const dt = e.dataTransfer
	if (dt?.files?.length) {
		const f = dt.files[0]
		if (f.type.startsWith('audio/')) {
			setFile(f)
		}
	}
}

function clearFile() {
	if (previewUrl.value) {
		URL.revokeObjectURL(previewUrl.value)
		previewUrl.value = null
	}
	file.value = null
	if (fileInput.value) {
		fileInput.value.value = ''
	}
}

async function onSubmit() {
	if (!file.value) return

	isLoading.value = true
	try {
		const blob = await convertAudio(file.value, format.value)
		const url = URL.createObjectURL(blob)
		const a = document.createElement('a')
		a.href = url
		a.download = `converted.${format.value}`
		a.click()
		URL.revokeObjectURL(url)
		clearFile()
	} catch (err) {
		console.error(err)
		alert('Failed to convert audio.')
	} finally {
		isLoading.value = false
	}
}

onUnmounted(() => {
	if (previewUrl.value) {
		URL.revokeObjectURL(previewUrl.value)
	}
})
</script>
