class ArticleManager {
  constructor(articleText, options = {}) {
    this.articleText = articleText;

    this.pages = [];
    this.words = 0;

    const defaultOptions = {
      wordsPerLine: 12,
      linesPerPage: 20,
      paymentStructure: {
        0: 0,
        1: 30,
        2: 30,
        3: 60,
        4: 60,
        'default': 100
      }
    }
    this.options = { ...defaultOptions, ...options }
  }

  splitIntoPages() {
    // Split the article into words
    this.words = this.articleText.trim().split(/\s+/);

    // Guarantee that if the article has no words, or if its empty then return early.
    if (this.words.length === 0 || this.words[0] === '') {
      this.pages = [];
      return;
    }

    // Separate into chunks to be able to handle it more efficiently.
    const lines = [];
    let chunkSize = this.options.wordsPerLine * this.options.linesPerPage; // 1 page per iteration
    let startIndex = 0;

    // First we get all the lines of the article
    while (startIndex < this.words.length) {
      const chunk = this.words.slice(startIndex, startIndex + chunkSize);
      const chunkLines = [];

      for (let i = 0; i < chunk.length; i += this.options.wordsPerLine) {
        chunkLines.push(chunk.slice(i, i + this.options.wordsPerLine).join(" "));
      }

      lines.push(...chunkLines);
      startIndex += chunkSize;
    }
    // We then set each 20 lines into a new page.
    this.pages = [];
    for (let i = 0; i < lines.length; i += this.options.linesPerPage) {
      this.pages.push(lines.slice(i, i + this.options.linesPerPage).join("\n"));
    }
  }

  calculatePayment() {
    // Clear payment structure based on the Options object.
    const paymentStructure = this.options.paymentStructure;
    const totalpages = this.pages.length;

    if (totalpages === 0) {
      return 0;
    }

    const payment = paymentStructure[totalpages] ?? paymentStructure["default"];
    return payment;
  }

  displayPages() {
    // To display the total pages, payment value, and each individual page on the console.
    const payment = this.calculatePayment();
    console.log(`Total Pages: ${this.pages.length}`);
    console.log(`Payment Due: $${payment}`);

    this.pages.forEach((page, index) => {
      console.log(`\nPage ${index + 1}:\n${page}\n`);
    });
  }

  processArticle() {
    // Make sure that the initial input is a string.
    try {
      if (typeof this.articleText !== "string") {
        throw new TypeError("Please make sure the input is a string.");
      }
    } catch (error) {
      console.error("Error:", error.message);
      return;
    }
    this.splitIntoPages();
    this.displayPages();
  }
}

// Example usage

articleText = `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Ut enim ad 
minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non 
proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Here is some more text just to test if it is 
working correctly. Your it to gave life whom as. Favourable dissimilar resolution led for and had. At play much to time
four many. Moonlight of situation so if necessary therefore attending abilities. Calling looking enquire up me to in 
removal. Park fat she nor does play deal our. Procured sex material his offering humanity laughing moderate can. 
Unreserved had she nay dissimilar admiration interested. Departure performed exquisite rapturous so ye me resources. 
As absolute is by amounted repeated entirely ye returned. These ready timed enjoy might sir yet one since. Years drift 
never if could forty being no. On estimable dependent as suffering on my. Rank it long have sure in room what as he. 
Possession travelling sufficient yet our. Talked vanity looked in to. Gay perceive led believed endeavor. Rapturous no
of estimable oh therefore direction up. Sons the ever not fine like eyes all sure.`

const articleManager = new ArticleManager(articleText);
articleManager.processArticle();