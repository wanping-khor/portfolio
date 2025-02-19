<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  let projects = writable([]); // 用 Svelte store 绑定数据
  let currentImageIndex = writable({}); // 记录每个项目的 index

  async function fetchProjects() {
    try {
      const res = await fetch("http://localhost:3000/api/projects");
      const data = await res.json();
      projects.set(data);
      // 初始化每个项目的图片索引
      let indexMap = {};
      data.forEach((project, i) => indexMap[i] = 0);
      currentImageIndex.set(indexMap);
    } catch (error) {
      console.error("Error fetching projects:", error);
    }
  }

  function nextImage(index, project) {
    currentImageIndex.update(imgIndexes => {
      imgIndexes[index] = (imgIndexes[index] + 1) % project.images.length;
      return imgIndexes;
    });
  }

  function prevImage(index, project) {
    currentImageIndex.update(imgIndexes => {
      imgIndexes[index] = (imgIndexes[index] - 1 + project.images.length) % project.images.length;
      return imgIndexes;
    });
  }

  onMount(fetchProjects);
</script>

<h2 class="section-title">Project Experience</h2>
<div class="projects-container">
  {#each $projects as project, index}
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
        <button on:click={() => prevImage(index, project)}>⬅</button>
        <img src={project.images[$currentImageIndex[index]]} alt="Screenshot of {project.title}" />
        <button on:click={() => nextImage(index, project)}>➡</button>
        <video controls>
          <source src={project.video} type="video/mp4" />
          <track src={project.captionSrc || "/files/empty_captions.vtt"} kind="captions" srclang="en" label="English" />
        </video>        
      </div>
    </div>
  {/each}
</div>
