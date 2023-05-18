document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var fileInput = document.getElementById("videoInput");
    var file = fileInput.files[0];

    if (file) {
      var reader = new FileReader();
      console.log(file);
      reader.onload = function (event) {
        var videoElement = document.createElement("video");
        videoElement.src = event.target.result;
        videoElement.controls = true;
        document.body.appendChild(videoElement);
      };
      reader.readAsDataURL(file);
    }
  });
