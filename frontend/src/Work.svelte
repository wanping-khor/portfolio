<script>
    import { onMount } from "svelte";
  
    export let workExperience = [];
  
    // Function to observe elements on scroll
    onMount(() => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
            }
          });
        },
        { threshold: 0.2 }
      );
  
      document.querySelectorAll(".work-card").forEach((el) => observer.observe(el));
    });
  </script>
  
  <div class="work-exp-container">
  <h2 class="section-title">Work Experience</h2>

  <div class="work-exp-list">
    {#each workExperience as work}
      <div class="work-card">
        <h3 class="work-position">{work.position}</h3>
        <p class="work-company">{work.company}</p>
        <p class="work-duration">{work.duration}</p>
        <ul class="work-scope">
          {#each work.job_scope as task}
            <li>{task}</li>
          {/each}
        </ul>
      </div>
    {/each}
  </div>
</div>