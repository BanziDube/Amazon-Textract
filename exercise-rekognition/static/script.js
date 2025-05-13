fetch('/data')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('results');

    for (const image in data) {
      const block = document.createElement('div');
      block.className = 'image-block';

      const title = document.createElement('h3');
      title.textContent = image;
      block.appendChild(title);

      const ul = document.createElement('ul');
      ul.className = 'labels';

      data[image].forEach(label => {
        const li = document.createElement('li');
        li.textContent = `${label.Name} (Confidence: ${label.Confidence.toFixed(2)}%)`;
        ul.appendChild(li);
      });

      block.appendChild(ul);
      container.appendChild(block);
    }
  })
  .catch(error => console.error('Error loading data.json:', error));
