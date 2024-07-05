document.addEventListener("DOMContentLoaded", function() {
    const candidateDivs = document.querySelectorAll(".each-info");
    const candidateModal = new bootstrap.Modal(document.getElementById('candidateModal'));
    const candidateNameElement = document.getElementById("candidateName");
    const candidateNumberElement = document.getElementById("candidateNumber");
    const candidateNumberInput = document.getElementById("candidate_number");
    const confirmVoteButton = document.getElementById("confirmVote");

    candidateDivs.forEach(div => {
        div.addEventListener("click", function() {
            const candidateNumber = this.getAttribute("data-number");
            const candidateName = this.querySelector("#name").textContent;

            candidateNameElement.textContent = candidateName;
            candidateNumberElement.textContent = candidateNumber;
            candidateNumberInput.value = candidateNumber;

            candidateModal.show();
        });
    });

    confirmVoteButton.addEventListener("click", function() {
        document.getElementById("voteForm").submit();
    });
});
