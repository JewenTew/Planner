# Planner

A lightweight project planner, similar to Microsoft Teams Planner, for tracking tasks and due dates across projects.

Single HTML file. No build step, no server, no dependencies to install.

## Features

- **Overview**: counts of overdue, due today and due this week across all plans, plus a list of tasks due in the next 14 days.
- **Board**: columns by bucket, with drag and drop. Can also group by due date, progress or priority. Quick add at the top of each column.
- **Grid**: sortable table of all tasks.
- **Schedule**: month calendar by due date.
- **Charts**: progress by bucket, priority and assignee.
- **Task details**: bucket, progress, priority, start and due date, assignee, labels, notes, checklist.
- Search and filters (due date, priority, hide completed).
- Light and dark theme, works on phone width.

## Usage

Open `index.html` in a browser.

## Data storage

- Opened directly from a file or any normal web host, data is saved in the browser's `localStorage`. It stays on that browser and device only, and is lost if browser data is cleared.
- When published as a Claude artifact, the page uses the artifact's shared database instead, so data syncs across devices and can be shared with teammates.
