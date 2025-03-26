<script>
  import { onMount } from "svelte";
  import { Button, Tooltip  } from 'flowbite-svelte';

  let projectExperience = [];
  let filteredProjects = [];
  let searchQuery = "";
  let selectedCategory = "All";
  let showVideo = false;

  const SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo";  
  const API_KEY = "AIzaSyCG4zhL2EJ_jJvZNxJ6GOh4RdjxJa99lGw";  
  const PROJECT_RANGE = "Sheet3!A1:G200";  

  async function fetchProjectExperience() {
      try {
          const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${PROJECT_RANGE}?key=${API_KEY}`);
          const data = await res.json();

          if (data.values) {
              projectExperience = data.values.slice(1).map(row => ({
                  project_title: row[0] || "Unknown project title",
                  subject_name: row[1] || "Unknown subject name",
                  position: row[2] || "Unknown position",
                  grade: row[3] || "N/A",
                  description: row[4] ? row[4].split("\n").map(task => task.trim()).filter(task => task !== "") : [],
                  category: row[5] || "Other",
                  demo: row[6] || null
              }));

              filteredProjects = [...projectExperience];
          }
      } catch (error) {
          console.error("Error fetching Work Experience data:", error);
      }
  }

  function applyFilters() {
      if (selectedCategory === "All" && searchQuery.trim() === "") {
          filteredProjects = [...projectExperience];
          return;
      }

      filteredProjects = projectExperience.filter(project => {
          const matchesSearch = searchQuery
              ? project.project_title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                project.subject_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                project.position.toLowerCase().includes(searchQuery.toLowerCase()) ||
                project.description.some(task => task.toLowerCase().includes(searchQuery.toLowerCase()))
              : true;

          const matchesCategory = selectedCategory === "All" || project.category.includes(selectedCategory);

          return matchesSearch && matchesCategory;
      });
  }

  onMount(fetchProjectExperience);
</script>

<div class="project-exp-container">
  <div class="project-filter-header">
  <h2 class="project-section-title">Project Experience</h2>
<!-- 
  <div class="edu-header">
    <strong class="edu-university">{edu.institution} ({edu.location})</strong>
    <div class="edu-year">{edu.duration}</div>
  </div> -->

  <!-- <div class="project-header"> -->
    <div class="filters">
      <input 
        type="text" 
        bind:value={searchQuery}
        on:input={applyFilters}
        placeholder="⌕  Search by position, subject name, project title or descriptions..."
        style="margin-top: 10px; width: 30rem; background-color: transparent; color: white"
      />
    
      <select bind:value={selectedCategory} on:change={applyFilters} style="margin-top: 10px; width: 10rem; background-color: transparent; color: white">
        <option value="All">All Categories</option>
        <option value="Analysis">Analysis</option>
        <option value="Develop">Develop</option>
      </select>
    </div>
  </div>

  {#if filteredProjects.length > 0}
      <div class="project-exp-list">
          {#each filteredProjects as project}
            <div class="project-card visible">
                <div class="project-header">
                    <h3 class="project-position">{project.project_title}</h3>
                    <p class="project-company">{project.position}  |  {project.subject_name}  | {project.grade} </p>
                    <!-- <p class="project-company">{project.subject_name}</p>
                    <p class="project-duration">{project.grade}</p> -->
                </div>
                <div class="project-content">
                  <ul class="project-scope">
                      {#each project.description as task}
                          <li>{task}</li>
                      {/each}
                  </ul>
                  {#if project.demo != null}
                    {#if project.demo == "mp4"}
                      <a class="view-demo-button" href={'/Demo/' + encodeURIComponent(project.project_title) + '.mp4'} target="_blank">View Demo</a>
                    {:else}
                      <a class="view-demo-button" href="/Demo/{project.project_title}.pdf" target="_blank">View Demo</a>
                    {/if}
                  {/if}
                </div>
              </div>
          {/each}
      </div>
  {:else}
      <p class="loading-message">No projects found...</p>
  {/if}
</div>