<script>
  import { onMount } from "svelte";
  import Work from "./Work.svelte";
  import Projects from "./Projects.svelte";

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

  let workExperience = [];
  let projects = [];

  let currentPage = "about";

  function changePage(page) {
    currentPage = page;
  }

  const SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo";  
  const API_KEY = "AIzaSyCG4zhL2EJ_jJvZNxJ6GOh4RdjxJa99lGw";  

  const PROFILE_RANGE = "Sheet1!A1:F200";  
  const WORK_RANGE = "Sheet2!A1:D200";  
  const PROJECT_RANGE = "Sheet3!A1:D200";  

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

  async function fetchProfileData() {
    try {
      const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${PROFILE_RANGE}?key=${API_KEY}`);
      const data = await res.json();

      if (data.values) {
        profile.name = data.values[1][0];
        profile.title = data.values[1][1];
        profile.location = data.values[1][2];
        profile.about = data.values[1][3];
        profile.image = data.values[1][4];

        profile.education = [];
        let educationIndex = data.values.findIndex(row => row[0] === "Education");
        if (educationIndex !== -1) {
          let educationData = data.values.slice(educationIndex + 1).filter(row => row.length > 1);
          profile.education = educationData.map(row => ({
            institution: row[0] || "N/A",
            location: row[1] || "N/A",
            course: row[2] || "N/A",
            major: row[3] || "N/A",
            CGPA: row[4] || "N/A",
            duration: row[5] || "N/A"
          }));
        }

        profile.skills = extractSection(data, "Skills");
        profile.achievements = extractSection(data, "Achievements");
        profile.languages = extractSection(data, "Languages");
        profile.interests = extractSection(data, "Interests");
      }
    } catch (error) {
      console.error("Error fetching Google Sheets data:", error);
    }
  }

  async function fetchWorkExperience() {
    try {
      const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${WORK_RANGE}?key=${API_KEY}`);
      const data = await res.json();

      if (data.values) {
        workExperience = data.values.slice(1).map(row => ({
          position: row[0] || "Unknown Position",
          company: row[1] || "Unknown Company",
          duration: row[2] || "N/A",
          job_scope: row[3] || "N/A"
        }));
      }
    } catch (error) {
      console.error("Error fetching Work Experience data:", error);
    }
  }

  async function fetchProjects() {
    try {
      const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${PROJECT_RANGE}?key=${API_KEY}`);
      const data = await res.json();

      if (data.values) {
        projects = data.values.slice(1).map(row => ({
          name: row[0] || "Unknown Project",
          description: row[1] || "No description available",
          tech: row[2] || "N/A"
        }));
      }
    } catch (error) {
      console.error("Error fetching Projects data:", error);
    }
  }

  onMount(() => {
    fetchProfileData();
    fetchWorkExperience();
    fetchProjects();
  });
</script>

<div class="container">
  <!-- Navigation Bar -->
  <nav class="navbar">
    <div class="nav-logo">My Portfolio</div>
    <div class="nav-links">
      <button class="nav-button" on:click={() => changePage('about')}>About</button>
      <button class="nav-button" on:click={() => changePage('work_exp')}>Work Experience</button>
      <button class="nav-button" on:click={() => changePage('project_exp')}>Project Experience</button>
      <button class="nav-button" on:click={() => changePage('contact')}>Contact</button>
    </div>
  </nav>

  {#if currentPage === "about"}
    <div class="card">
      <div class="profile-header">
        <div class="profile-img" style="background-image: url({profile.image})"></div>
        <div>
          <h1>{profile.name}</h1>
          <h2>{profile.title}</h2>
          <p class="location">{profile.location}</p>
        </div>
      </div>

      <h2 class="section-title">About</h2>
      <p class="section-content">{profile.about}</p>

      <h2 class="section-title">Education</h2>
      <div class="education-box">
        {#if profile.education.length > 0}
          <ul class="list">
            {#each profile.education as edu}
              <li class="edu-item">
                <strong class="edu-university">{edu.institution} ({edu.location})</strong>
                <div class="edu-degree">{edu.course}</div>
                {#if edu.major !== "N/A"}
                  <div class="edu-major">Major: {edu.major}</div>
                {/if}
                {#if edu.CGPA !== "N/A"}
                  <div class="edu-cgpa">CGPA: {edu.CGPA}</div>
                {/if}
                <div class="edu-year">{edu.duration}</div>
              </li>
            {/each}
          </ul>
        {/if}
      </div>

      <h2 class="section-title">Skills</h2>
      <div class="skills-box">
        {#each profile.skills as skill}
          <div class="skill-item">{skill}</div>
        {/each}
      </div>

      <h2 class="section-title">Achievements</h2>
      <div class="achievements-box">
        {#each profile.achievements as achievement}
          <p>{achievement}</p>
        {/each}
      </div>

      <h2 class="section-title">Languages</h2>
      <div class="languages-box">
        {#each profile.languages as language}
          <span class="language-badge">{language}</span>
        {/each}
      </div>

      <h2 class="section-title">Interests</h2>
      <div class="interests-box">
        {#each profile.interests as interest}
          <p>{interest}</p>
        {/each}
      </div>
    </div>

  {:else if currentPage === "work_exp"}
    <Work {workExperience} />

  {:else if currentPage === "project_exp"}
    <Projects {projects} />
  {/if}
</div>
