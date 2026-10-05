// Scontorna le persone in una foto con Vision di macOS (nessun servizio esterno).
// Uso: swift new_logo/sorgente/scontorna.swift <foto.jpg> <uscita.png>
import AppKit
import CoreImage
import Vision

let args = CommandLine.arguments
guard args.count == 3,
      let image = CIImage(contentsOf: URL(fileURLWithPath: args[1])) else {
    print("uso: scontorna.swift <foto> <uscita.png>")
    exit(1)
}

let request = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: image)
try handler.perform([request])
guard let result = request.results?.first else {
    print("nessuna persona trovata")
    exit(2)
}

// tutte le istanze trovate (due dottori = due istanze), maschera alla risoluzione della foto
let buffer = try result.generateMaskedImage(ofInstances: result.allInstances, from: handler, croppedToInstancesExtent: false)
let masked = CIImage(cvPixelBuffer: buffer)
let context = CIContext()
guard let cg = context.createCGImage(masked, from: masked.extent) else { exit(3) }
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
print("ok \(result.allInstances.count) istanze")
