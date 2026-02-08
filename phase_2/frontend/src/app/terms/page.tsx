export default function TermsPage() {
  return (
    <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Terms of Service</h1>
        <div className="prose prose-gray max-w-none">
          <p className="text-gray-600">
            These terms govern your use of the Todo App service.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">Acceptance of Terms</h2>
          <p className="text-gray-600">
            By accessing or using the Todo App service, you agree to be bound by these Terms of Service.
            If you disagree with any part of the terms, then you may not access the service.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">Use License</h2>
          <p className="text-gray-600">
            Permission is granted to temporarily download one copy of the materials on Todo App
            for personal, non-commercial transitory viewing only.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">Disclaimer</h2>
          <p className="text-gray-600">
            The materials on Todo App are provided on an 'as is' basis. Todo App makes no warranties,
            expressed or implied, and hereby disclaims and negates all other warranties including,
            without limitation, implied warranties or conditions of merchantability, fitness for
            a particular purpose, or non-infringement of intellectual property.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">Limitations</h2>
          <p className="text-gray-600">
            In no event shall Todo App or its suppliers be liable for any damages arising out of
            the use or inability to use the materials on Todo App website.
          </p>
        </div>
      </div>
    </div>
  );
}