const lbAvant = document.getElementById('lb-avant')
const lbTrigger = document.querySelector('.hero-avant-wrap')
if (lbAvant && lbTrigger) {
  const lbImg = lbAvant.querySelector('.lb-img')
  const openLb = () => { lbAvant.hidden = false; document.body.style.overflow = 'hidden' }
  const closeLb = () => { lbAvant.hidden = true; document.body.style.overflow = '' }
  lbTrigger.addEventListener('click', openLb)
  lbTrigger.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb() } })
  lbAvant.addEventListener('click', (e) => { if (e.target !== lbImg) closeLb() })
  lbAvant.querySelector('.lb-close').addEventListener('click', closeLb)
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLb() })
}

document.querySelectorAll('[data-scroll]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'))
    if (!target) return
    event.preventDefault()
    target.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
})

document.body.classList.add('has-sticky-cta')

const revealItems = document.querySelectorAll('section, .card, .quote, .gallery figure')
revealItems.forEach((item) => item.classList.add('reveal'))

const observer = 'IntersectionObserver' in window
  ? new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        entry.target.classList.add('is-visible')
        observer.unobserve(entry.target)
      })
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' })
  : null

if (observer) {
  revealItems.forEach((item) => observer.observe(item))
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'))
}

const forms = document.querySelectorAll('[data-estimate-form]')
forms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()
    const data = new FormData(form)
    const subject = encodeURIComponent('Demande de soumission peinture Terrebonne')
    const body = encodeURIComponent(
      `Nom: ${data.get('name') || ''}\nTelephone: ${data.get('phone') || ''}\nCourriel: ${data.get('email') || ''}\nService: ${data.get('service') || ''}\nMessage: ${data.get('message') || ''}`
    )
    window.location.href = `mailto:soumission@peintureterrebonne.ca?subject=${subject}&body=${body}`
  })
})
