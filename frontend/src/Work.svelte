  <script>
    export let workExperience = [];
  </script>
  
  <div class="work-exp-container">
    <h2 class="section-title">Work Experience</h2>
  
    {#if workExperience.length > 0}
      <div class="work-exp-list">
        {#each workExperience as work}
          <div class="work-card">
            <h3 class="work-position">{work.position}</h3>
            <p class="work-company">{work.company}</p>
            <p class="work-duration">📅 {work.duration}</p>
            <ul class="work-scope">
              {#each work.job_scope as task}
                <li>✅ {task}</li>
              {/each}
            </ul>
          </div>
        {/each}
      </div>
    {:else}
      <p class="empty-message">No work experience available.</p>
    {/if}
  </div>
  
  <style>
    .work-exp-container {
      padding: 20px;
      color: white;
    }
  
    .section-title {
      font-size: 24px;
      margin-bottom: 15px;
      color: white;
    }
  
    .work-exp-list {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
  
    .work-card {
      background: #fff;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
  
    .work-position {
      font-size: 18px;
      font-weight: bold;
      color: white;
    }
  
    .work-company {
      font-size: 16px;
      color: #555;
      margin: 5px 0;
    }
  
    .work-duration {
      font-size: 14px;
      color: #666;
    }
  
    .work-scope {
      margin-top: 10px;
      padding-left: 20px;
    }
  
    .work-scope li {
      font-size: 14px;
      color: #444;
    }
  
    .empty-message {
      text-align: center;
      color: #888;
    }
  </style>
  