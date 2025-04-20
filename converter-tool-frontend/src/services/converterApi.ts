import axios from 'axios'

export async function convertImage(
	file: File,
	format: string,
): Promise<Blob> {
	const form = new FormData();
	form.append('image', file);
	form.append('format', format);

	const response = await axios.post<Blob>(
		'/convert-image',
		form,
		{ responseType: 'blob' },
	);

	return response.data;
}

export async function convertAudio(
	file: File,
	format: string,
): Promise<Blob> {
	const form = new FormData();
	form.append('audio_file', file);
	form.append('format', format);

	const response = await axios.post<Blob>(
		'/convert-audio',
		form,
		{ responseType: 'blob' },
	);

	return response.data;
}
