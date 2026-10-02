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
- **My Day**: pick tasks from any plan to work on today; the list clears itself every night.
- **Search all plans** from the Overview.
- **Undo**: deleting tasks or a plan shows an Undo button for 10 seconds (or press Ctrl + Z).
- **Reminders**: the installed app shows the number of overdue and due-today tasks on its icon, and a summary when you open it each day.
- **Links**: attach links (assignment brief, Google Drive, Teams) to a task and open them in one click.
- **Custom order**: drag cards up and down inside a column (Sort: Custom).
- **Archive plans**: hide finished classes or projects without deleting them; restore any time.
- **Keyboard shortcuts**: N new task, / search, 1 to 4 switch views, Esc close, ? show the list.
- **Repeating tasks**: daily, weekdays, weekly, every 2 weeks or monthly. Completing one adds the next.
- **Backup and restore**: export everything to a `.json` file and import it on another computer or browser.
- Search and filters (due date, priority, hide completed).
- Multi-select: select tasks one by one, a whole column, or everything shown, then delete or mark complete in one go.
- English and Chinese, switch with the EN / 中 button. English by default.
- White, pale pink and pale blue light theme by default, with an optional dark theme (sun / moon switch). Works on phone width.

## Usage

Open https://jewentew.github.io/Planner/ (GitHub Pages), or open `index.html` in a browser.

### Install as an app

The page is an installable web app with its own icon, and it opens offline.

- Edge or Chrome on a computer: open the page, then menu, Apps, Install this site as an app.
- Phone: open the page in the browser, then Add to Home screen.

### Cloud sync (optional)

Fill in `firebase-config.js` with a Firebase web app's settings to turn on Google sign-in and sync through Firestore. Each user's data lives under `users/{uid}` and the Firestore rules only let that user read or write it:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

Add the GitHub Pages domain under Authentication, Settings, Authorized domains. With `apiKey` left empty, the app runs without sign-in and keeps data in the browser.

## Data storage

Use **Backup & restore** in the sidebar to export a backup file now and then.


- Signed in (cloud sync on), data is saved in Firestore under your account and syncs across devices.
- Not signed in, data is saved in the browser's `localStorage`. It stays on that browser and device only, and is lost if browser data is cleared.
- When published as a Claude artifact, the page uses the artifact's shared database instead, so data syncs across devices.
