<script>
    import { onMount } from "svelte";
    import { Button, Tooltip  } from 'flowbite-svelte';
  
    let profile = {
      name: "Loading...",
      title: "Loading...",
      location: "Loading...",
      image: "https://via.placeholder.com/150",
      about: "Fetching data...",
      education: [],
      skills: [],
      achievements: [],
      languages: [],
      interests: []
    };
  
    const SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo";  
    const API_KEY = "AIzaSyCG4zhL2EJ_jJvZNxJ6GOh4RdjxJa99lGw";  
    const PROFILE_RANGE = "Sheet1!A1:F200";  
  
    async function fetchProfileData() {
    try {
      const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${PROFILE_RANGE}?key=${API_KEY}`);
      const data = await res.json();

      if (data.values) {
        profile = {  
          name: data.values[1]?.[0] || "Unknown",
          title: data.values[1]?.[1] || "Unknown",
          location: data.values[1]?.[2] || "Unknown",
          about: data.values[1]?.[3] || "No information",
          image: data.values[1]?.[4] || "https://via.placeholder.com/150",
          education: extractEducation(data),
          skills: extractSection(data, "Skills"),
          achievements: extractSection(data, "Achievements"),
          languages: extractSection(data, "Languages"),
          interests: extractSection(data, "Interests")
        };
      }
    } catch (error) {
      console.error("Error fetching Google Sheets data:", error);
    }
  }

  function extractEducation(data) {
    let startIndex = data.values.findIndex(row => row[0] === "Education");
    if (startIndex === -1) return [];

    let educationData = data.values.slice(startIndex + 1);
    let formattedEducation = [];

    for (let i = 0; i < educationData.length; i++) {
      let row = educationData[i];

      if (row.length >= 6) {
        formattedEducation.push({
          institution: row[0] || "Unknown",
          location: row[1] || "Unknown",
          course: row[2] || "Unknown",
          major: row[3] || "N/A",
          CGPA: row[4] || "N/A",
          duration: row[5] || "Unknown"
        });
      }
    }

    return formattedEducation;
  }
  
    function extractSection(data, sectionName) {
      let startIndex = data.values.findIndex(row => row[0] === sectionName);
      if (startIndex === -1) return [];
  
      let nextHeaderIndex = data.values.findIndex((row, index) => 
        index > startIndex && ["Education", "Skills", "Achievements", "Languages", "Interests"].includes(row[0])
      );
  
      let sectionData = nextHeaderIndex === -1 
        ? data.values.slice(startIndex + 1)
        : data.values.slice(startIndex + 1, nextHeaderIndex);
  
      return sectionData.map(row => row[0]).filter(Boolean);
    }
  
    onMount(() => {
      fetchProfileData();
    });
  </script>
  
  <div class="card">
    <div class="profile-header">
      <div class="profile-img" style="background-image: url({profile.image})"></div>
      <div>
        <h1>{profile.name}</h1>
        <h2>{profile.title}</h2>
        <p class="location">{profile.location}</p>
      </div>
    </div>

    <h2 class="about-section-title">About</h2>
    <p class="section-content">{profile.about}</p>

    <h2 class="about-section-title">Education</h2>
    <div class="education-box">
      {#if profile.education.length > 0}
        <ul class="list">
          {#each profile.education as edu}
          <li class="edu-item">
            <div class="edu-header">
              <strong class="edu-university">{edu.institution} ({edu.location})</strong>
              <div class="edu-year">{edu.duration}</div>
            </div>
            <div class="edu-degree">{edu.course}</div>
            {#if edu.major !== "N/A"}
              <div class="edu-major">Major: {edu.major}</div>
            {/if}
            <div class="edu-bottom">
              {#if edu.CGPA !== "N/A"}
                <div class="edu-cgpa">CGPA: {edu.CGPA}</div>
              {/if}
              <div class="edu-buttons">
                <!-- <a class="view-btn" href="/documents/degree_certificate.pdf" target="_blank">
                View Certificate
              </a>
              <a class="download-btn" href="/documents/degree_certificate.pdf" download>
                Download Certificate
              </a> -->
                <a class="view-btn" href="/documents/Transcript.pdf" target="_blank">View Transcript</a>
                <!-- <a class="download-btn" href="/documents/Transcript.pdf" download> -->
                  <!-- Download Transcript -->
                <!-- </a> -->
              </div>
            </div>
          </li>
          {/each}
        </ul>
      {/if}
    </div>
    

    <!-- Skills -->
    <h2 class="about-section-title">Skills</h2>
    <div class="skills-box">
      {#each profile.skills as skill}
        <div class="skill-item">
          <img src={`/icon/${skill}.png`} alt="{skill} icon" />
          {skill}
        </div>
      {/each}
    </div>

    <!-- Achievements -->
    <h2 class="about-section-title">Achievements</h2>
    <div class="achievements-box">
      {#each profile.achievements as achievement}
        <div class="achievement-item">
          <img src={`/icon/achievement.png`} alt="achievement icon" />
          <Button href="/Documents/${achievement}.pdf" class="achievement-button">{achievement}</Button>
          <!-- <Tooltip placement='right'>Click to view certificate</Tooltip> -->
          <!-- <p>{achievement}</p> -->
        </div>
      {/each}
    </div>

    <!-- Languages -->
    <h2 class="about-section-title">Languages</h2>
    <div class="languages-box">
      {#each profile.languages as language}
        <span class="language-badge">{language}</span>
      {/each}
    </div>

      <!-- Interests -->
      <h2 class="about-section-title">Interests</h2>
      <div class="interests-box">
        {#each profile.interests as interest}
          <div class="interest-item">
            <span class="interest-icon">🎯</span>
            <p>{interest}</p>
          </div>
        {/each}
      </div>
    </div>