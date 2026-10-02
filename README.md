# Planner

A lightweight planner, similar to Microsoft Teams Planner, for keeping track of homework, projects and due dates. Built for school now and work later.

Single HTML file. No build step, no server, no dependencies to install.

## Features

- **Overview**: counts of overdue, due today and due this week across all plans, a week or month calendar with due dates from every plan, and a list of tasks due in the next 14 days.
- **Board**: columns by bucket, with drag and drop. Reorder buckets by dragging the column title or with the arrow buttons. Can also group by due date, progress or priority. Quick add at the top of each column.
- **Grid**: sortable table of all tasks.
- **Schedule**: month calendar by due date.
- **Charts**: progress by bucket, priority and person.
- **Task details**: bucket, progress, priority, start and due date, assigned person, labels, notes, checklist.
- **Repeating tasks**: daily, weekdays, weekly, every 2 weeks or monthly. Completing one adds the next.
- **Backup and restore**: export everything to a `.json` file and import it on another computer or browser.
- Search and filters (due date, priority, hide completed).
- Multi-select: select tasks one by one, a whole column, or everything shown, then delete or mark complete in one go.
- English and Chinese, switch with the EN / 中 button. English by default.
- White, pale pink and pale blue light theme by default, with an optional dark theme (sun / moon switch). Works on phone width.

## Usage

Open `index.html` in a browser, or turn on GitHub Pages for this repository and open the Pages link.

## Data storage

Use **Backup & restore** in the sidebar to export a backup file now and then.


- Opened directly from a file or any normal web host, data is saved in the browser's `localStorage`. It stays on that browser and device only, and is lost if browser data is cleared.
- When published as a Claude artifact, the page uses the artifact's shared database instead, so data syncs across devices.
