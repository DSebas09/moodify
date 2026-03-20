const input       = document.getElementById("track_name");
const hiddenId    = document.getElementById("track_id");
const dropdown    = document.getElementById("autocomplete-results");
const searchForm  = document.getElementById("search-form");

const MIN_CHARS         = 2;
const DEBOUNCE_DELAY_MS = 350;

/**
 * Returns a debounced version of fn that fires after `delay` ms of inactivity.
 * @param {Function} fn
 * @param {number} delay
 * @returns {Function}
 */
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

function showDropdown() {
  dropdown.style.display = "block";
}

function hideDropdown() {
  dropdown.style.display = "none";
  dropdown.innerHTML = "";
}

function clearSelection() {
  hiddenId.value = "";
}

async function fetchSuggestions(query) {
  const res   = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  const data  = await res.json();
  return data.items ?? [];
}

function buildItem(track) {
  const el = document.createElement("div");
  el.className = "autocomplete-item";
  el.dataset.trackId = track.track_id;
  el.innerHTML = `
    <div class="fw-semibold text-dark small">${track.track_name}</div>
    <div class="text-muted" style="font-size: 0.8rem;">${track.artists}</div>
  `;
  return el;
}

function renderDropdown(items) {
  dropdown.innerHTML = "";

  if (items.length === 0) {
    dropdown.innerHTML = `
      <div class="autocomplete-item text-muted small">
        No results found.
      </div>`;
    showDropdown();
    return;
  }

  items.forEach((track) => {
    const el = buildItem(track);
    el.addEventListener("mousedown", () => selectTrack(track));
    dropdown.appendChild(el);
  });

  if (items.length >= MIN_CHARS) {
    const more = document.createElement("div");
    more.className = "autocomplete-item text-center border-top";
    more.innerHTML = `<span class="small text-primary fw-semibold">Ver todos los resultados →</span>`;
    more.addEventListener("mousedown", () => {
      clearSelection();
      hideDropdown();
      searchForm.submit();
    });
    dropdown.appendChild(more);
  }

  showDropdown();
}

function selectTrack(track) {
  input.value    = track.track_name;
  hiddenId.value = track.track_id;
  hideDropdown();
}

let activeIndex = -1;

function getItems() {
  return Array.from(dropdown.querySelectorAll(".autocomplete-item"));
}

function setActive(items, index) {
  items.forEach((el) => el.classList.remove("active"));
  if (index >= 0 && index < items.length) {
    items[index].classList.add("active");
    activeIndex = index;
  }
}

input.addEventListener("keydown", (e) => {
  const items = getItems();
  if (!items.length) return;

  if (e.key === "ArrowDown") {
    e.preventDefault();
    setActive(items, Math.min(activeIndex + 1, items.length - 1));
  }

  if (e.key === "ArrowUp") {
    e.preventDefault();
    setActive(items, Math.max(activeIndex - 1, 0));
  }

  if (e.key === "Enter" && activeIndex >= 0) {
    e.preventDefault();
    const active = items[activeIndex];
    if (active?.dataset?.trackId) {
      selectTrack({
        track_name: active.querySelector(".fw-semibold").textContent,
        artists:    active.querySelector(".text-muted").textContent,
        track_id:   active.dataset.trackId,
      });
      searchForm.submit();
    }
  }

  if (e.key === "Escape") {
    hideDropdown();
  }
});

const onInput = debounce(async (e) => {
  const query = e.target.value.trim();
  clearSelection();
  activeIndex = -1;

  if (query.length < MIN_CHARS) {
    hideDropdown();
    return;
  }

  const items = await fetchSuggestions(query);
  renderDropdown(items);
}, DEBOUNCE_DELAY_MS);

input.addEventListener("input", onInput);


