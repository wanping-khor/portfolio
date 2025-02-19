<script>
  import { onMount } from "svelte";
  let projects = [];
  let currentImageIndex = 0;

  async function fetchProjects() {
    const res = await fetch("http://localhost:3000/api/projects");
    projects = await res.json();
  }

  function nextImage(project) {
    currentImageIndex = (currentImageIndex + 1) % project.images.length;
  }

  function prevImage(project) {
    currentImageIndex = (currentImageIndex - 1 + project.images.length) % project.images.length;
  }

  onMount(fetchProjects);
</script>

<h2 class="section-title">Project Experience</h2>
<div class="projects-container">
  {#each projects as project, index}
    <div class="project-box {index % 2 === 0 ? 'left' : 'right'}">
      <div class="project-content">
        <h3>{project.title}</h3>
        <ul>
          {#each project.description as desc}
            <li>{desc}</li>
          {/each}
        </ul>
        <a class="download-btn" href={project.downloadLink} download>Download</a>
      </div>
      <div class="media">
        <button on:click={() => prevImage(project)}>⬅</button>
        <img src={project.images[currentImageIndex]} alt="Screenshot of {project.title}" />
        <button on:click={() => nextImage(project)}>➡</button>
        <video controls>
          <source src={project.video} type="video/mp4" />
          <track src={project.captionSrc || "/files/empty_captions.vtt"} kind="captions" srclang="en" label="English" />
        </video>        
      </div>
    </div>
  {/each}
</div>