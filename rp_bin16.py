#I just copy pasted the fit for one transit and run several times..

n = jdtot.size
t = jdtot-np.median(jdtot)
tbin_16 = np.transpose(bin16_lcs)
params_lcs = []
file_lcs=open('planet1_1_lcs.pic','w')
for i in tbin_16:
    #now let's get the MCMC initialized
    #initial guesses for MCMC fit parameters from your by eye fits
    #for simplicity we will only fit for Rp/R*, limb darkening coefficient, and center of transit time
    guess_rp, guess_u, guess_t0 = 0.12, 0.4, 0.003
    theta = [guess_rp, guess_u, guess_t0]
    flux= i
    err = 100.e-6  #100 ppm noise 
    flux = flux + np.random.normal(0, err, n)
    ndim, nwalkers = len(theta), 50
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args = (params, m, t, flux, err))
    pos = [theta + 1e-5*np.random.randn(ndim) for i in range(nwalkers)]

    #run mcmc
    sampler.run_mcmc(pos,500);
    #make a pairs plot from MCMC output
    samples = sampler.chain[:, 80:, :].reshape((-1, ndim)) #discard first 50 samples as burn-in
    fig = corner.corner(samples, labels = ["rp", "u", "t0"])
    plt.show()

    #Now we need to derive the best-fit planet parameters and their 1-sigma error bars
    rp_mcmc, u_mcmc, t0_mcmc = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), zip(*np.percentile(samples, [16, 50, 84], axis=0)))
    params_lcs.append([rp_mcmc,u_mcmc,t0_mcmc])
    
    
    print rp_mcmc
    print u_mcmc
    print t0_mcmc

#the next is not necessary at all. but it helped me keep short the ploting lines =)
rps,rp_ex,rp_ey=[],[],[]
ups,up_ex,up_ey=[],[],[]

for i in range(0,len(params_lcs)):
    rps.append(params_lcs[i][0][0])
    rp_ex.append(params_lcs[i][0][1])
    rp_ey.append(params_lcs[i][0][2])
    ups.append(params_lcs[i][1][0])
    up_ex.append(params_lcs[i][1][1])
    up_ey.append(params_lcs[i][1][2])


plt.figure()
plt.errorbar(w16,rps,xerr=rp_ex,yerr=rp_ey)
plt.xlabel(r'Wavelength [$\mu$m]')
plt.ylabel(r'R$_p$/R$_S$')

plt.savefig('radius.eps')
plt.savefig('radius.png')
plt.figure()
plt.errorbar(w16,ups,xerr=up_ex,yerr=up_ey)
plt.xlabel(r'Wavelength [$\mu$m]')
plt.ylabel('u')
#plt.savefig('limb_dark.eps')
plt.savefig('limb_dark.png')
plt.show()
