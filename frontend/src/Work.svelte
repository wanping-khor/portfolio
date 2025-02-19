<script>
    import { onMount } from "svelte";

    let workExperience = [];

    const SHEET_ID = "1LGYnrT2sZDdPVUdij5m45V9qB8lqjNBRXYPmh6GdPvo";  
    const API_KEY = "AIzaSyCG4zhL2EJ_jJvZNxJ6GOh4RdjxJa99lGw";  
    const WORK_RANGE = "Sheet2!A1:D200";  

    async function fetchWorkExperience() {
        try {
            const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${WORK_RANGE}?key=${API_KEY}`);
            const data = await res.json();

            if (data.values) {
                workExperience = data.values.slice(1).map(row => ({
                    position: row[0] || "Unknown Position",
                    company: row[1] || "Unknown Company",
                    duration: row[2] || "N/A",
                    job_scope: row[3] ? row[3].split("\n").map(task => task.trim()).filter(task => task !== "") : []
                }));
            }
        } catch (error) {
            console.error("Error fetching Work Experience data:", error);
        }
    }

    // Observe elements for animation
    onMount(() => {
        fetchWorkExperience();

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

        setTimeout(() => {
            document.querySelectorAll(".work-card").forEach((el) => observer.observe(el));
        }, 1000); // Ensure elements exist before observing
    });
</script>

<div class="work-exp-container">
    <h2 class="section-title">Work Experience</h2>

    {#if workExperience.length > 0}
        <div class="work-exp-list">
            {#each workExperience as work}
                <div class="work-card">
                    <div class="work-header">
                        <h3 class="work-position">{work.position}</h3>
                        <p class="work-company">{work.company}</p>
                        <p class="work-duration">{work.duration}</p>
                    </div>
                    <ul class="work-scope">
                        {#each work.job_scope as task}
                            <li>{task}</li>
                        {/each}
                    </ul>
                </div>
            {/each}
        </div>
    {:else}
        <p class="loading-message">Fetching work experience...</p>
    {/if}
</div>