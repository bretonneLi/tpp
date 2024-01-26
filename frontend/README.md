# Tingyimiao TPP react wordpress App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
It integrates with wordpress plugin.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

### `build a wp plugin`

when build a wordpress plugin, you need to make change to index.js(line 10), import the specified page to the root html tag, and then run build.

### `deploy to Wordpress`

1. After run 'npm run build', all the plugin file will be ready in build folder.
2. Create a new folder in \wordpress\wp-content\plugins\****.
3. Copy php file, templates folder and build folder, paste to folder **** .
4. Activate the plugin in the wp-admin plugin page.