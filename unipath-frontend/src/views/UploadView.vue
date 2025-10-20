<template>
  <div class="container">
    <h1>🎓 Upload Resume</h1>

    <input type="file" @change="onFileChange" accept=".pdf" />
    <button :disabled="!file" @click="uploadResume">Upload</button>

    <div v-if="loading" class="loading">⏳ Processing your resume...</div>

    <div v-if="result">
<!--       <h2>🧠 Summary</h2>
      <pre>{{ result.summary }}</pre> -->
      <!-- 🧠 Summary Section -->
<div v-if="result?.summary" class="summary-section">
  <h2>🧠 1. Applicant Background Summary</h2>

  <!-- Field -->
  <div class="summary-block">
    <h3>🎓 Field</h3>
    <p>{{ result.summary.field }}</p>
  </div>

  <!-- Education -->
  <div class="summary-block" v-if="result.summary.education?.length">
    <h3> 📖 Education</h3>
    <ul>
      <li v-for="(edu, i) in result.summary.education" :key="i">{{ edu }}</li>
    </ul>
  </div>

  <!-- Skills -->
  <div class="summary-block" v-if="result.summary.skills?.length">
    <h3>🛠️ Skills</h3>
    <div class="skills">
      <span v-for="(skill, i) in result.summary.skills" :key="i" class="skill-tag">{{ skill }}</span>
    </div>
  </div>

  <!-- Experience -->
  <div class="summary-block" v-if="result.summary.experience?.length">
    <h3>💼 Experience</h3>
    <ul>
      <li v-for="(exp, i) in result.summary.experience" :key="i">{{ exp }}</li>
    </ul>
  </div>

  <!-- Interests -->
  <div class="summary-block" v-if="result.summary.interests?.length">
    <h3>💡 Research Interests</h3>
    <ul>
      <li v-for="(interest, i) in result.summary.interests" :key="i">{{ interest }}</li>
    </ul>
  </div>

  <!-- Publications -->
  <div class="summary-block" v-if="result.summary.publications?.length">
    <h3>📚 Publications</h3>
    <ul>
      <li v-for="(pub, i) in result.summary.publications" :key="i">{{ pub }}</li>
    </ul>
  </div>
</div>


      <div v-if="result?.recommendations?.programs?.recommended_programs" class="summary-section">
      <h2>🎯2.  Recommended Programs</h2>
      <div v-for="(p, i) in result.recommendations.programs.recommended_programs" :key="i" class="program-card">
        <h3 >{{ p.title }}</h3>
        <p>{{ p.snippet }}</p>
        <a :href="p.link" target="_blank">More Program Related Links</a>
      </div>
      <h4>🔗 verify Related Links</h4>
    <ul class="summary-block" >
      <li
        v-for="(url, i) in result.recommendations.faculty.links"
        :key="i"
      >
        <a :href="url" target="_blank" rel="noopener noreferrer">{{ url }}</a>
      </li>
    </ul>
      </div>
    </div>

    <div v-if="result?.recommendations?.programs?.recommended_programs" class="summary-section">
        <h2>🔥 3. Faculty Matches </h2>


      <div v-if="result.recommendations.faculty.faculty_matches" class="summary-block">
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
.summary-section {
  background: #f9fafb;
  border-radius: 16px;
  padding: 24px;
  margin-top: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.summary-section h2 {
  font-size: 1.6rem;
  margin-bottom: 16px;
  color: #1e293b;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 4px;
}

.summary-block {
  margin-bottom: 20px;
}

.summary-block h3 {
  font-size: 1.1rem;
  color: #2563eb;
  margin-bottom: 8px;
}

.summary-block ul {
  list-style-type: "– ";
  padding-left: 1rem;
  color: #374151;
}

.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.skill-tag {
  background: #e0f2fe;
  color: #0369a1;
  padding: 6px 10px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
}
</style>