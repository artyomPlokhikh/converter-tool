<template>
	<div class="max-w-md mx-auto w-full p-4">
		<h2 class="text-xl mb-4">Convert an Image</h2>

		<form @submit.prevent="onSubmit" class="space-y-4">
			<div v-if="!previewUrl">
				<div
					@dragover.prevent="isDragActive = true"
					@dragleave.prevent="isDragActive = false"
					@drop.prevent="onDrop"
					:class="['relative w-full h-64 flex items-center justify-center rounded border-2 border-dashed cursor-pointer transition-colors', isDragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300 bg-white']"
				>
					<input
						ref="fileInput"
						type="file"
						accept="image/*"
						class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
						@change="onFileChange"
					/>
					<p class="text-gray-500 text-center px-4">
						Click or drag & drop an image here
					</p>
				</div>
			</div>

			<div
				v-else
				class="relative mt-4 w-full h-64"
			>
				<img
					:src="previewUrl"
					alt="Image preview"
					class="w-full h-full object-contain border rounded"
				/>

				<button
					@click="clearFile"
					type="button"
					class="absolute top-0 right-0 m-2 z-10 bg-gray-800 bg-opacity-50 hover:bg-opacity-75 text-white rounded-full p-1 cursor-pointer"
					aria-label="Clear image"
				>
					<x-mark-icon class="h-4 w-4"/>
				</button>
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
				class="w-full bg-blue-600 text-white py-2 rounded cursor-pointer disabled:opacity-50"
			>
				Convert
			</button>
		</form>
	</div>
</template>

<script lang="ts" setup>
import { ref, onUnmounted } from 'vue'
import { convertImage } from '@/services/converterApi'
import XMarkIcon from "@/components/icons/XMarkIcon.vue";

interface FormatOption {
	value: string
	label: string
}

const file = ref<File | null>(null);
const previewUrl = ref<string | null>(null);
const isDragActive = ref(false);
const format = ref<string>('PNG');
const fileInput = ref<HTMLInputElement>();
const isLoading = ref(false);

const formats = <FormatOption[]>[
	{ value: 'JPEG', label: 'JPEG' },
	{ value: 'BMP', label: 'BMP' },
	{ value: 'GIF', label: 'GIF' },
	{ value: 'PNG', label: 'PNG' },
	{ value: 'ICO', label: 'ICO' },
];

function setFile(f: File) {
	if (previewUrl.value) {
		URL.revokeObjectURL(previewUrl.value);
	}
	file.value = f;
	previewUrl.value = URL.createObjectURL(f);
}

function onFileChange(e: Event) {
	const input = e.target as HTMLInputElement
	if (input.files && input.files[0]) {
		setFile(input.files[0]);
	}
}

function clearFile() {
	if (previewUrl.value) {
		URL.revokeObjectURL(previewUrl.value)
		previewUrl.value = null
	}
	if (fileInput.value) {
		fileInput.value.value = '';
	}
	file.value = null;
}

function onDrop(e: DragEvent) {
	isDragActive.value = false;
	const dt = e.dataTransfer;
	if (dt?.files?.length) {
		const f = dt.files[0];
		if (f.type.startsWith('image/')) {
			setFile(f);
		}
	}
}

async function onSubmit() {
	if (!file.value) return;

	isLoading.value = true;
	try {
		const blob = await convertImage(file.value, format.value);
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `converted.${format.value.toLowerCase()}`;
		a.click();
		URL.revokeObjectURL(url);
		clearFile();
	} catch (err) {
		console.error(err);
		alert('Failed to convert image.');
	} finally {
		isLoading.value = false;
	}
}

onUnmounted(() => {
	if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
})
</script>
