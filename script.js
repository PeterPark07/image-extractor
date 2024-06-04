const urlForm = document.getElementById('url-form');
const extractedImages = document.getElementById('extracted-images');

urlForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const url = document.getElementById('url').value;

  fetch(url)
    .then(response => response.text())
    .then(htmlContent => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(htmlContent, 'text/html');
      const images = doc.querySelectorAll('img');

      extractedImages.innerHTML = ''; // Clear previous results

      images.forEach(img => {
        const imageElement = document.createElement('img');
        imageElement.src = img.src;
        extractedImages.appendChild(imageElement);
      });
    })
    .catch(error => {
      console.error('Error fetching images:', error);
      extractedImages.innerHTML = 'Failed to extract images.';
    });
});
