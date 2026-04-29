// ===============================
// HABITS DATA
// ===============================
const habits = [
  {
    title: "1. Define Your Style Goals",
    text: "Dress with intention. Know how you want to feel and what your style communicates.",
    image: "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?auto=format&fit=crop&w=1600&q=80"
  },
  {
    title: "2. Learn What Flatters You",
    text: "Understanding fit and color builds confidence and simplifies shopping.",
    image: "https://images.unsplash.com/photo-1520975916090-3105956dac38?auto=format&fit=crop&w=1600&q=80"
  },
  {
    title: "3. Invest in Quality Pieces",
    text: "Timeless staples create a strong and versatile wardrobe foundation.",
    image: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=1600&q=80"
  },
  {
    title: "4. Edit Your Wardrobe",
    text: "Remove what no longer aligns with your personal style.",
    image: "https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?auto=format&fit=crop&w=1600&q=80"
  },
  {
    title: "5. Plan Outfits Ahead",
    text: "Planning reduces stress and improves daily presentation.",
    image: "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=1600&q=80"
  },
  {
    title: "6. Stay Open to Growth",
    text: "Let your style evolve with your lifestyle and confidence.",
    image: "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=1600&q=80"
  },
  {
    title: "7. Prioritize Fit",
    text: "Perfect fit always looks better than chasing trends.",
    image: "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1600&q=80"
  }
];

let current = 0;
let interval;

// ===============================
// BUILD MODAL CONTENT
// ===============================
const modalBox = document.querySelector(".modal-box");
modalBox.innerHTML = "";
modalBox.style.background = "transparent";

modalBox.innerHTML = `
  <div class="habit-container">
      <div class="habit-image" id="habitImage">
          <button class="habit-close" id="habitClose">&times;</button>
          <div class="habit-textbox">
              <h2 id="habitTitle"></h2>
              <p id="habitText"></p>
          </div>
      </div>
  </div>
`;

const imageLayer = document.getElementById("habitImage");
const titleEl = document.getElementById("habitTitle");
const textEl = document.getElementById("habitText");

// ===============================
// SLIDE FUNCTION
// ===============================
function showSlide(index) {
  imageLayer.style.opacity = "0";

  setTimeout(() => {
    imageLayer.style.backgroundImage = `url('${habits[index].image}')`;
    titleEl.textContent = habits[index].title;
    textEl.textContent = habits[index].text;
    imageLayer.style.opacity = "1";
  }, 300);
}

function startSlides() {
  showSlide(current);
  interval = setInterval(() => {
    current = (current + 1) % habits.length;
    showSlide(current);
  }, 2000);
}

// ===============================
// EVENTS
// ===============================
const modal = document.getElementById("habitModal");

document.getElementById("habitLink").addEventListener("click", e => {
  e.preventDefault();
  modal.style.display = "flex";
  current = 0;
  startSlides();
});

document.getElementById("showHabits").addEventListener("click", () => {
  modal.style.display = "flex";
  current = 0;
  startSlides();
});

document.getElementById("habitClose").addEventListener("click", () => {
  modal.style.display = "none";
  clearInterval(interval);
});

// ===============================
// STYLES
// ===============================
const style = document.createElement("style");
style.innerHTML = `
/* center everything */
.habit-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* main image (50% screen) */
.habit-image {
  width: 60%;
  height: 60%;
  background-size: cover;
  background-position: center;
  border-radius: 20px;
  position: relative;
  transition: opacity 0.4s ease;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* close button */
.habit-close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 28px;
  background: rgba(0,0,0,0.6);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
}

/* text box */
.habit-textbox {
  background: rgba(255,255,255,0.9);
  padding: 30px 40px;
  border-radius: 15px;
  max-width: 500px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.habit-textbox h2 {
  font-size: 24px;
  margin-bottom: 15px;
}

.habit-textbox p {
  font-size: 16px;
  line-height: 1.6;
}
`;
document.head.appendChild(style);