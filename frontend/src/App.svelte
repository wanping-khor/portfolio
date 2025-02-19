<script>
  import Router  from "svelte-spa-router";
  import routes from "./routes.js";
</script>

<div class="container">
  <!-- Navigation Bar -->
  <nav class="navbar">
    <div class="nav-logo">My Portfolio</div>
    <div class="nav-links">
      <a class="nav-button" href="#/">About</a>
      <a class="nav-button" href="#/work_exp">Work Experience</a>
      <a class="nav-button" href="#/project_exp">Project Experience</a>
    </div>
  </nav>

  <Router {routes} />
</div>
