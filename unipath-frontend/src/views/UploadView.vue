<template>
  <div class="container">
    <h1>🎓 Upload Resume</h1>

    <input type="file" @change="onFileChange" accept=".pdf" />
    <button :disabled="!file" @click="uploadResume">Upload</button>

    <div v-if="loading" class="loading">⏳ Processing your resume...</div>

    <div v-if="result">
      <h2>🧠 Summary</h2>
      <pre>{{ result.summary }}</pre>

      <div v-if="result?.recommendations?.programs?.recommended_programs">
      <h2>🎯 Recommended Programs</h2>
      <div v-for="(p, i) in result.recommendations.programs.recommended_programs" :key="i" class="program-card">
        <h3>{{ p.title }}</h3>
        <p>{{ p.snippet }}</p>
        <a :href="p.link" target="_blank">View Program Official webpage</a>
      </div>
      </div>
    </div>

    <div v-if="result?.recommendations?.programs?.recommended_programs">
        <h2>🔥 Faculty Matches </h2>
      <div v-if="result.recommendations.faculty.faculty_matches">
        <div v-for="(prof, i) in result.recommendations.faculty.faculty_matches" :key="i" class="program-card">
          <h3>{{ prof.name }}</h3>
          <p><strong>{{ prof.title }}</strong></p>
          <p>{{ prof.research }}</p>
        </div>
      </div>
         <!-- Faculty Links -->
  <div
    v-if="result.recommendations.faculty.links && result.recommendations.faculty.links.length"
    class="faculty-links"
  >
    <h4>🔗 More Related Links</h4>
    <ul>
      <li
        v-for="(url, i) in result.recommendations.faculty.links"
        :key="i"
      >
        <a :href="url" target="_blank" rel="noopener noreferrer">{{ url }}</a>
      </li>
    </ul>
  </div>
  </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const file = ref(null);
const result = ref(null);
const loading = ref(false);

function onFileChange(e) {
  file.value = e.target.files[0];
}

async function uploadResume() {
  if (!file.value) return;
  loading.value = true;

  const formData = new FormData();
  formData.append("file", file.value);

  try {
    const res = await fetch("http://127.0.0.1:8000/upload-resume", {
      method: "POST",
      body: formData,
    });
    result.value = await res.json();
  } catch (err) {
    console.error("❌ Upload failed:", err);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 50px auto;
  text-align: center;
  font-family: sans-serif;
}
button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #0077ff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.program-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  margin: 10px 0;
  text-align: left;
}
.loading {
  margin: 20px 0;
  font-style: italic;
}
</style>
