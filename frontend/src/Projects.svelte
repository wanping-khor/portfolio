<script>
    export let projects = [];
  </script>
  
  <h2 class="section-title">Project Experience</h2>
  <ul class="list">
    {#each projects as project}
      <li>{project}</li>
    {/each}
  </ul>
  