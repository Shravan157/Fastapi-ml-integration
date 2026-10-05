/**
 * HealthPredict Frontend Logic
 * Implements routing, patient management, and mock ML predictions.
 */

// --- Mock Data ---
const MOCK_PATIENTS = [
    { id: 'P-1001', name: 'Sarah Jenkins', age: 62, risk: 'low', lastVisit: '2023-10-12' },
    { id: 'P-1002', name: 'Michael Chen', age: 45, risk: 'medium', lastVisit: '2023-10-20' },
    { id: 'P-1003', name: 'Emily Rodriguez', age: 71, risk: 'high', lastVisit: '2023-11-01' },
    { id: 'P-1004', name: 'David Smith', age: 38, risk: 'low', lastVisit: '2023-10-28' },
    { id: 'P-1005', name: 'Jessica Lee', age: 54, risk: 'medium', lastVisit: '2023-11-05' },
    { id: 'P-1006', name: 'Robert Wilson', age: 68, risk: 'high', lastVisit: '2023-10-15' },
    { id: 'P-1007', name: 'Linda Taylor', age: 50, risk: 'low', lastVisit: '2023-11-08' },
    { id: 'P-1008', name: 'James Moore', age: 59, risk: 'medium', lastVisit: '2023-10-30' },
];

// --- State Management ---
let currentPatientFilter = '';

// --- DOM Elements ---
const elements = {
    navLinks: document.querySelectorAll('.nav-link'),
    pages: document.querySelectorAll('.page'),
    patientList: document.getElementById('patient-list'),
    patientSearch: document.getElementById('patient-search'),
    predictionForm: document.getElementById('prediction-form'),
    resultDisplay: document.getElementById('result-display'),
    resultPlaceholder: document.querySelector('.result-placeholder'),
    resultContent: document.querySelector('.result-content'),
    riskBadge: document.getElementById('risk-badge'),
    riskScore: document.getElementById('risk-score'),
    riskDesc: document.getElementById('risk-desc'),
};

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    renderPatients();
    setupPrediction();

    // Handle deep linking
    const hash = window.location.hash;
    if (hash) {
        const target = hash.substring(1);
        switchPage(target);
    }
});

// --- Navigation Logic ---
function setupNavigation() {
    elements.navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('data-target');
            switchPage(target);

            // Update URL hash
            window.location.hash = target;
        });
    });
}

function switchPage(pageId) {
    elements.pages.forEach(page => {
        page.classList.remove('active');
        if (page.id === pageId) {
            page.classList.add('active');
        }
    });

    elements.navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-target') === pageId) {
            link.classList.add('active');
        }
    });
}

// --- Patient Management ---
function renderPatients(filter = '') {
    if (!elements.patientList) return;
    elements.patientList.innerHTML = '';

    const filtered = MOCK_PATIENTS.filter(p =>
        p.name.toLowerCase().includes(filter.toLowerCase()) ||
        p.id.toLowerCase().includes(filter.toLowerCase())
    );

    filtered.forEach(patient => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${patient.id}</td>
            <td style="font-weight: 500;">${patient.name}</td>
            <td>${patient.age}</td>
            <td><span class="risk-pill ${patient.risk}">${patient.risk}</span></td>
            <td>${patient.lastVisit}</td>
            <td>
                <button class="btn-action" onclick="alert('Viewing ${patient.name}')">View</button>
                <button class="btn-action" onclick="alert('Editing ${patient.name}')">Edit</button>
            </td>
        `;
        elements.patientList.appendChild(tr);
    });
}

if (elements.patientSearch) {
    elements.patientSearch.addEventListener('input', (e) => {
        renderPatients(e.target.value);
    });
}

// --- Prediction Engine ---
function setupPrediction() {
    if (!elements.predictionForm) return;
    elements.predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI Loading state
        const btn = e.target.querySelector('button');
        const originalText = btn.innerText;
        btn.innerText = 'Processing...';
        btn.disabled = true;

        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());

        try {
            // In a real app, this would be:
            // const response = await fetch('/predict', {
            //     method: 'POST',
            //     body: JSON.stringify(data),
            //     headers: { 'Content-Type': 'application/json' }
            // });
            // const result = await response.json();

            // Mocked Prediction Logic
            await new Promise(resolve => setTimeout(resolve, 800)); // Simulate network lag

            const riskScore = Math.floor(Math.random() * 100);
            const prediction = calculateRisk(riskScore);

            displayResult(prediction);
        } catch (err) {
            console.error('Prediction error:', err);
            alert('An error occurred while processing the prediction.');
        } finally {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    });
}

function calculateRisk(score) {
    if (score < 30) {
        return {
            level: 'low',
            label: 'Low Risk',
            score: `${score}% Probability`,
            desc: 'The patient shows minimal risk indicators. Continue routine monitoring.'
        };
    } else if (score < 70) {
        return {
            level: 'medium',
            label: 'Medium Risk',
            score: `${score}% Probability`,
            desc: 'The patient shows moderate risk indicators. Follow-up screening is recommended.'
        };
    } else {
        return {
            level: 'high',
            label: 'High Risk',
            score: `${score}% Probability`,
            desc: 'Significant risk indicators detected. Immediate clinical review required.'
        };
    }
}

function displayResult(result) {
    if (!elements.resultPlaceholder || !elements.resultContent) return;
    elements.resultPlaceholder.classList.add('hidden');
    elements.resultContent.classList.remove('hidden');

    if (elements.riskBadge) {
        elements.riskBadge.innerText = result.label;
        elements.riskBadge.className = `risk-badge ${result.level}`;
    }
    if (elements.riskScore) {
        elements.riskScore.innerText = result.score;
    }
    if (elements.riskDesc) {
        elements.riskDesc.innerText = result.desc;
    }
}

// Define in global scope for the HTML button
window.resetPrediction = function() {
    if (elements.resultPlaceholder && elements.resultContent) {
        elements.resultPlaceholder.classList.remove('hidden');
        elements.resultContent.classList.add('hidden');
    }
    if (elements.predictionForm) {
        elements.predictionForm.reset();
    }
};
